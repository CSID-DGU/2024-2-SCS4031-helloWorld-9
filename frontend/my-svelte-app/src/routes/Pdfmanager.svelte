<script>
  import { onMount } from 'svelte';
  import { Filemanager } from "wx-svelte-filemanager";
  import { Willow } from "wx-svelte-filemanager";
  import * as pdfjsLib from 'pdfjs-dist/build/pdf';
  import { fileManagerState, pdfContents, driveInfo, statusMessage } from '../store.js';
  
  let api;
  pdfjsLib.GlobalWorkerOptions.workerSrc = '/node_modules/pdfjs-dist/build/pdf.worker.mjs';
  const server = "https://some-backend-url";
  let rawData = [];
  
  // 파일 매니저 초기화
  function init(fileManagerApi) {
    api = fileManagerApi;
    
    // 컨텍스트 메뉴 커스터마이징
    api.intercept("context-menu", (action) => {
      const defaultMenu = action.menu;
      defaultMenu.push({
        id: "upload-pdf",
        text: "PDF 업로드",
        icon: "wxi-file-upload"
      });
      return defaultMenu;
    });
  
    // 파일 업로드 처리
    api.on("upload-pdf", async ({ id: targetFolder }) => {
      const input = document.createElement('input');
      input.type = 'file';
      input.multiple = true;
      input.accept = '.pdf';
      
      input.onchange = async (event) => {
        const files = event.target.files;
        await processPdfFiles(files, targetFolder);
      };
      
      input.click();
    });
  }
  
  function loadData(ev) {
    const id = ev.detail.id;
    statusMessage.set('파일 데이터를 불러오는 중입니다...');

    fetch(server + "/files?id=" + encodeURIComponent(id))
      .then((response) => {
        if (!response.ok) {
          throw new Error(`서버 오류: ${response.status} ${response.statusText}`);
        }
        return response.json();
      })
      .then((data) => {
        api.exec("provide-data", { data, parent: id });
        statusMessage.set('파일 데이터를 성공적으로 불러왔습니다.');
      })
      .catch((error) => {
        statusMessage.set(`오류 발생: ${error.message}`);
      });
  }

  // 초기 데이터 로드
  $: {
    statusMessage.set('초기 파일 데이터를 불러오는 중입니다...');
    
    fetch(server + "/files")
      .then((response) => {
        if (!response.ok) {
          throw new Error(`서버 오류: ${response.status} ${response.statusText}`);
        }
        return response.json();
      })
      .then((data) => {
        rawData = data;
        statusMessage.set('초기 데이터를 성공적으로 불러왔습니다.');
      })
      .catch((error) => {
        statusMessage.set(`오류 발생: ${error.message}`);
      });
  }
  
  // PDF 파일 처리
  async function processPdfFiles(files, targetFolder) {
    statusMessage.set('파일을 처리하는 중입니다...');
  
    for (const file of files) {
      try {
        const arrayBuffer = await file.arrayBuffer();
        const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
        let content = '';
  
        for (let i = 0; i < pdf.numPages; i++) {
          const page = await pdf.getPage(i + 1);
          const textContent = await page.getTextContent();
          content += textContent.items.map(item => item.str).join(' ') + '\n';
        }
  
        // 파일 매니저에 파일 추가
        const fileId = `${targetFolder}/${file.name}`;
        api.exec("provide-data", {
          parent: targetFolder,
          data: [{
            id: fileId,
            type: "file",
            size: file.size,
            date: new Date(),
            ext: "pdf"
          }]
        });
  
        // PDF 내용 저장
        pdfContents.update(contents => ({
          ...contents,
          [fileId]: { content, filename: file.name }
        }));
  
        // 드라이브 정보 업데이트
        driveInfo.update(info => ({
          ...info,
          used: info.used + file.size
        }));
  
        statusMessage.set(`${file.name} 파일이 성공적으로 업로드되었습니다.`);
      } catch (error) {
        statusMessage.set(`Error processing ${file.name}: ${error.message}`);
      }
      
    }
  }
  
  // 파일 매니저 상태 변경 시 store 업데이트
  function handleStateChange() {
    if (api) {
      const state = api.getState();
      fileManagerState.set({
        structure: api.serialize(),
        activePanel: state.activePanel,
        mode: state.mode,
        currentPath: state.path
      });
    }
  }
  
  // 컴포넌트 마운트 시 저장된 상태 복원
  onMount(() => {
    let state;
    fileManagerState.subscribe(value => {
      state = value;
    })();
  
    if (state.structure.length > 1) {
      api.exec("provide-data", {
        parent: "/",
        data: state.structure
      });
    }
  });
</script>
  
  <div class="file-manager-container">
    <Willow>
      <Filemanager
        {init}
        mode="cards"
        icons="simple"
        data={rawData}
        on:data-request={loadData}
        on:change={handleStateChange}
        drive={$driveInfo}
      />
    </Willow>
    
    <div class="status-message">
      {$statusMessage}
    </div>
  </div>
  
  <style>
    .file-manager-container {
      width: 100%;
      height: 80vh;
      display: flex;
      flex-direction: column;
    }
  
    .status-message {
      padding: 10px;
      margin-top: 10px;
      background-color: #f5f5f5;
      border-radius: 4px;
      font-size: 14px;
    }
  </style>