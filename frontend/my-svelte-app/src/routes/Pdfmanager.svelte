<script>
  import { onMount } from 'svelte';
  import { Filemanager } from "wx-svelte-filemanager";
  import { Willow } from "wx-svelte-filemanager";
  import * as pdfjsLib from 'pdfjs-dist/build/pdf';
  import { RestDataProvider } from "wx-filemanager-data-provider";
  import { fileManagerState, pdfContents, driveInfo, statusMessage } from '../store.js';

  let api;
  pdfjsLib.GlobalWorkerOptions.workerSrc = '/node_modules/pdfjs-dist/build/pdf.worker.mjs';

  let rawData = [];
  let isLoading = true; 

  const fileserver_url = "/api/fileserver";
  const restProvider = new RestDataProvider(fileserver_url);

  // 파일 매니저 초기화
  function init(fileManagerApi) {
    api = fileManagerApi;

    api.setNext(restProvider);

    statusMessage.set('파일 매니저 로드 완료');

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

  $: data = [];
  $: drive = {};

  Promise.all([restProvider.loadFiles(), restProvider.loadInfo()]).then(([files, info]) => {
    data = files;
    drive = info;
    isLoading = false; // true로 바꾸면 로딩 상태를 확인할 수 있습니다.
  });

  $: {
    console.log("Updated drive:", drive);
  }
</script>

<div class="file-manager-container">
  <Willow>
    <Filemanager
      {init}
      bind:api
      mode="cards"
      icons="simple"
      {data}
      {drive}
    />
  </Willow>

  <div class="loading-overlay" style="display: {isLoading ? 'flex' : 'none'};"> 
    <div class="loading-icon"></div>
  </div>  

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
    position: relative; /* 로딩 애니메이션 오버레이를 위해 추가 */
  }

  .loading-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(255, 255, 255, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 10; /* 파일 매니저 위에 표시되도록 설정 */
  }

  .loading-icon {
    width: 40px;
    height: 40px;
    border: 4px solid rgba(0, 0, 0, 0.1);
    border-top: 4px solid #3498db;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }

  .status-message {
    padding: 10px;
    margin-top: 10px;
    background-color: #f5f5f5;
    border-radius: 4px;
    font-size: 14px;
  }
</style>
