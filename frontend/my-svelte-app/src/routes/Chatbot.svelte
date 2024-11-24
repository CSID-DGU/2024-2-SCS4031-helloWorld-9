<script>
  import { writable } from 'svelte/store';
  import { pdfContents, fileManagerState, statusMessage } from '../store.js';

  const API_KEY = import.meta.env.VITE_OPENAI_API_KEY;
  let questionText = '';
  let answerText = '';

  // fileManagerState에서 모든 PDF 파일 목록을 가져오는 함수
  function getPdfFiles() {
    return $fileManagerState.structure.filter(item => 
      item.type === 'file' && item.id.toLowerCase().endsWith('.pdf')
    );
  }

  // 모든 PDF 파일의 내용을 가져오는 함수
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

  async function askChatbot() {
    console.log("질문하기 버튼이 클릭되었습니다.");

    if (!questionText) {
      answerText = "질문을 입력해주세요.";
      return;
    }

    const pdfContent = getAllPdfContent();
    if (!pdfContent) {
      answerText = "분석할 PDF 파일이 없습니다. 먼저 PDF 파일을 업로드해주세요.";
      return;
    }

    const fullInput = `다음 PDF 파일들의 내용을 참고하여 질문에 답변해주세요:\n\n${pdfContent}\n\n질문: ${questionText}`;

    try {
      const response = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${API_KEY}`
        },
        body: JSON.stringify({
          model: 'gpt-3.5-turbo',
          messages: [{ role: 'user', content: fullInput }]
        })
      });

      if (!response.ok) {
        answerText = `Error: ${response.status} ${response.statusText}`;
        return;
      }

      const data = await response.json();
      if (data.choices && data.choices.length > 0) {
        answerText = data.choices[0].message.content;
      } else {
        answerText = "API 응답에서 답변을 찾을 수 없습니다.";
      }
    } catch (error) {
      answerText = `Error: ${error.message}`;
    }
  }
</script>

<div class="card">
  <h2>챗봇</h2>
  <div class="file-info">
    <h3>현재 로드된 PDF 파일 목록:</h3>
    <ul>
      {#each getPdfFiles() as file}
        <li>{file.id.split('/').pop()}</li>
      {/each}
    </ul>
  </div>
  <textarea 
    bind:value={questionText} 
    placeholder="PDF 문서의 내용에 대해 궁금한 점을 물어보세요"
    class="question-input"
  ></textarea>
  <button class="button-primary" on:click={askChatbot}>질문하기</button>
  {#if answerText}
    <div class="answer">
      <h3>답변:</h3>
      <p>{answerText}</p>
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

  .button-primary:hover {
    background-color: #0056b3;
  }

  .answer {
    margin-top: 20px;
    padding: 15px;
    background-color: #f8f9fa;
    border-radius: 5px;
  }

  .answer h3 {
    margin-top: 0;
    color: #333;
  }

  .answer p {
    margin: 10px 0 0 0;
    line-height: 1.5;
  }
</style>