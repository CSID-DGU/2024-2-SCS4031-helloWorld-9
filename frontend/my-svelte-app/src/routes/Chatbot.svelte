<!-- Chatbot.svelte -->
<script>
  import { writable } from 'svelte/store';
  import { pdfContents, fileManagerState, statusMessage } from '../store.js';

  let questionText = '';
  let answerText = '';
  let references = [];
  let isLoading = false;

  // PDF 파일 관련 함수들 (주석 처리)
  /*
  function getPdfFiles() {
    return $fileManagerState.structure.filter(item => 
      item.type === 'file' && item.id.toLowerCase().endsWith('.pdf')
    );
  }

  function getAllPdfContent() {
    let content = '';
    const pdfFiles = getPdfFiles();
    
    pdfFiles.forEach((file) => {
      const pdfContent = $pdfContents[file.id];
      if (pdfContent) {
        content += `파일 이름: ${pdfContent.filename}\n${pdfContent.content}\n\n`;
      }
    });
    
    return content;
  }
  */

  async function askChatbot() {
    if (!questionText) {
      answerText = "질문을 입력해주세요.";
      return;
    }

    /* PDF 파일 체크 부분 주석 처리
    const pdfContent = getAllPdfContent();
    if (!pdfContent) {
      answerText = "분석할 PDF 파일이 없습니다. 먼저 PDF 파일을 업로드해주세요.";
      return;
    }
    */

    isLoading = true;
    try {
      // 여기를 8000 포트로 수정
      const response = await fetch('http://localhost:8000/api/chatbot/get-answer', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          question: questionText
        })
      });


      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      answerText = data.answer;
      references = data.references || [];
    } catch (error) {
      answerText = `Error: ${error.message}`;
      references = [];
    } finally {
      isLoading = false;
    }
  }
</script>

<div class="card">
  <h2>챗봇</h2>
  <!-- PDF 파일 목록 표시 부분 주석 처리 -->
  <!--
  <div class="file-info">
    <h3>현재 로드된 PDF 파일 목록:</h3>
    <ul>
      {#each getPdfFiles() as file}
        <li>{file.id.split('/').pop()}</li>
      {/each}
    </ul>
  </div>
  -->
  
  <textarea 
    bind:value={questionText} 
    placeholder="PDF 문서의 내용에 대해 궁금한 점을 물어보세요"
    class="question-input"
  ></textarea>
  <button class="button-primary" on:click={askChatbot} disabled={isLoading}>
    {isLoading ? '처리 중...' : '질문하기'}
  </button>
  
  {#if answerText}
    <div class="answer">
      <h3>답변:</h3>
      <p>{answerText}</p>
    </div>
  {/if}
  
  {#if references.length > 0}
    <div class="references">
      <h3>참조 문서:</h3>
      {#each references as ref}
        <div class="reference-item">
          <p class="source">출처: {ref.source}</p>
          <p class="content">{ref.content}</p>
        </div>
      {/each}
    </div>
  {/if}
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

  /* 주석 처리된 파일 정보 스타일 유지 */
  /*
  .file-info {
    margin: 15px 0;
    padding: 10px;
    background-color: #f8f9fa;
    border-radius: 5px;
  }

  .file-info ul {
    list-style-type: none;
    padding-left: 0;
  }

  .file-info li {
    margin: 5px 0;
    color: #666;
  }
  */

  .question-input {
    width: 100%;
    min-height: 100px;
    padding: 10px;
    margin: 10px 0;
    border: 1px solid #ddd;
    border-radius: 5px;
    resize: vertical;
  }

  .button-primary {
    background-color: #007bff;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    margin: 10px 0;
  }

  .button-primary:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
  }

  .button-primary:hover:not(:disabled) {
    background-color: #0056b3;
  }

  .answer {
    margin-top: 20px;
    padding: 15px;
    background-color: #f8f9fa;
    border-radius: 5px;
  }

  .references {
    margin-top: 20px;
    padding: 15px;
    background-color: #f5f5f5;
    border-radius: 5px;
  }

  .reference-item {
    margin: 10px 0;
    padding: 10px;
    background-color: white;
    border-radius: 4px;
    border: 1px solid #ddd;
  }

  .source {
    font-weight: bold;
    color: #666;
    margin-bottom: 5px;
  }

  .content {
    white-space: pre-wrap;
    color: #333;
  }
</style>