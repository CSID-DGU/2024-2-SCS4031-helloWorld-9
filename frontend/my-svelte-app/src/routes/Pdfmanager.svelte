<script>
  import { onMount } from 'svelte';
  import { Filemanager } from "wx-svelte-filemanager";
  import { Willow } from "wx-svelte-filemanager";
  import * as pdfjsLib from 'pdfjs-dist/build/pdf';
  import { fileManagerState, pdfContents, driveInfo, statusMessage } from '../store.js';
  
  let api;
  pdfjsLib.GlobalWorkerOptions.workerSrc = '/node_modules/pdfjs-dist/build/pdf.worker.mjs';

  let rawData = [];
  
  // 파일 매니저 초기화
  function init(fileManagerApi) {
    api = fileManagerApi;
  
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

  $: {
    fetch("/api/files")
      .then((data) => data.json())
      .then((data) => (rawData = data))
      .then((data)=>{
        console.log(data);
        statusMessage.set(data.files);
      })
  }
  
</script>
  
  <div class="file-manager-container">
    <Willow>
      <Filemanager
        {init}
        bind:api
        mode="cards"
        icons="simple"
        data={rawData}
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