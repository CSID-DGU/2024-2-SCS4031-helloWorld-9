<script>
  import { writable } from 'svelte/store';
  import { pdfContents, loadedFiles } from '../store.js'; // 전역 스토어 가져오기

  const API_KEY = import.meta.env.VITE_OPENAI_API_KEY;
  let questionText = '';
  let answerText = '';

    // 모든 PDF 파일의 내용을 가져오는 함수
    function getAllPdfContent() {
    let content = '';
    Object.values($pdfContents).forEach((file) => {
        content += `파일 이름: ${file.filename}\n${file.content}\n\n`;
    });
    return content;
    }


async function askChatbot() {
  console.log("질문하기 버튼이 클릭되었습니다."); // 함수가 실행되면 이 메시지가 콘솔에 출력됩니다.

  if (!questionText) {
    answerText = "질문을 입력해주세요.";
    return;
  }

  const pdfContent = getAllPdfContent();
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
  <textarea bind:value="{questionText}" placeholder="궁금한 점을 물어보세요"></textarea>
  <button class="button-primary" on:click="{askChatbot}">질문하기</button>
  <p class="answer">답변: {answerText}</p>
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

  .button-primary {
    background-color: #007bff;
    color: white;
    padding: 10px 15px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    margin-top: 5px;
  }

  .button-primary:hover {
    background-color: #0056b3;
  }

  .answer {
    margin-top: 10px;
    font-size: 16px;
  }
</style>
