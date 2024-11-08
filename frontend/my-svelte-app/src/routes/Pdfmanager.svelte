<script>
  import { onMount } from 'svelte';
  import { pdfContents, loadedFiles, statusMessage } from '../store.js';
  import * as pdfjsLib from 'pdfjs-dist/build/pdf';

  onMount(() => {
    pdfjsLib.GlobalWorkerOptions.workerSrc = '/node_modules/pdfjs-dist/build/pdf.worker.mjs';
  });

  async function processPdf(files) {
    statusMessage.set('파일을 처리하는 중입니다...');

    for (const file of files) {
      const fileReader = new FileReader();
      fileReader.onload = async (event) => {
        const fileName = file.name;
        const pdfData = event.target.result;

        if (!pdfContents[fileName]) {
          try {
            const pdf = await pdfjsLib.getDocument({ data: pdfData }).promise;
            let content = '';

            for (let i = 0; i < pdf.numPages; i++) {
              const page = await pdf.getPage(i + 1);
              const textContent = await page.getTextContent();
              content += textContent.items.map(item => item.str).join(' ') + '\n';
            }

            pdfContents.update(contents => ({ ...contents, [fileName]: { content, filename: fileName } }));
            loadedFiles.update(files => [...files, fileName]);
            statusMessage.set(`성공적으로 처리된 파일: ${fileName}`);
          } catch (error) {
            statusMessage.set(`Error processing ${fileName}: ${error.message}`);
          }
        } else {
          statusMessage.set('이미 업로드된 파일입니다.');
        }
      };
      fileReader.readAsArrayBuffer(file);
    }
  }

  function removePdf(filename) {
    pdfContents.update(contents => {
      const updatedContents = { ...contents };
      delete updatedContents[filename];
      return updatedContents;
    });

    loadedFiles.update(files => files.filter(file => file !== filename));
    statusMessage.set(`${filename} 파일이 삭제되었습니다.`);
  }
</script>

<div class="card">
  <h2>PDF 파일 관리</h2>
  <input type="file" multiple on:change="{(event) => processPdf(event.target.files)}" />
  <p class="status">{$statusMessage}</p>

  <h3>로드된 파일 목록</h3>
  <ul>
    {#each $loadedFiles as file}
      <li>
        {file} 
        <button class="button-secondary" on:click="{() => removePdf(file)}">삭제</button>
      </li>
    {/each}
  </ul>
</div>

<style>
  .card {
    background-color: #fff;
    border-radius: 8px;
    border: 2px solid #d3d3d3;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    padding: 20px;
    margin-bottom: 20px;
  }

  .button-secondary {
    background-color: #6c757d;
    color: white;
    padding: 5px 10px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }

  .button-secondary:hover {
    background-color: #5a6268;
  }

  .status {
    margin-top: 10px;
    font-size: 14px;
    color: #666;
  }
</style>
