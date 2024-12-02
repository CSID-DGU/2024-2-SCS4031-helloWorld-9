<script>
  import { onMount, onDestroy } from 'svelte';
  import { Filemanager } from "wx-svelte-filemanager";
  import { Willow } from "wx-svelte-filemanager";
  import * as pdfjsLib from 'pdfjs-dist/build/pdf';
  import { RestDataProvider } from "wx-filemanager-data-provider";
  import { fileManagerState, pdfContents, driveInfo, statusMessage } from '../store.js';
  
  
  let api;
  let eventSource;
  pdfjsLib.GlobalWorkerOptions.workerSrc = '/node_modules/pdfjs-dist/build/pdf.worker.mjs';

  let rawData = [];

  const fileserver_url = "/api/fileserver";
  const restProvider = new RestDataProvider(fileserver_url);
  
  // 파일 매니저 초기화
  function init(fileManagerApi) {
    api = fileManagerApi;
    
    api.setNext(restProvider);
  
    // statusMessage.set('파일 매니저 로드 완료');
  
  }

  function connectSSE() {
    if (eventSource) {
      eventSource.close(); // 기존 연결 해제
    }

    eventSource = new EventSource("/api/sse/sse_test");

    eventSource.onmessage = (event) => {
      console.log("SSE Message:", event.data);
      statusMessage.set(event.data); // 메시지 업데이트
    };

    eventSource.onerror = (error) => {
      console.error("SSE Error:", error);
      statusMessage.set("SSE 연결이 끊겼습니다. 재연결 중...");

      // 연결 해제 및 5초 후 재연결 시도
      eventSource.close();
      setTimeout(() => {
        connectSSE();
      }, 5000);
    };
  }

  onMount(() => {
    connectSSE();

    return () => {
      if (eventSource) {
        eventSource.close();
        console.log("SSE connection closed.");
      }
    };
  });

  onDestroy(() => {
    if (eventSource) {
      eventSource.close();
      console.log("SSE connection destroyed.");
    }
  });
  $: data = [];
  $: drive = {};

  Promise.all([restProvider.loadFiles(), restProvider.loadInfo()])
  .then(([files, info]) => {
    data = files;
    drive = info;
    statusMessage.set(`Loaded ${files.length} files.`);
  })
  .catch((error) => {
    statusMessage.set(`Error loading data: ${error.message || error}`);
  });


  $: if (api) {
    api.on("select-file", ({ id }) => {
      if(id!=null)
        statusMessage.set(`선택 : ${id}`);
    });
    api.on("create-file", ({ parent, file }) => {
      statusMessage.set(`${file.name} 업로드 중...`);
      });
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