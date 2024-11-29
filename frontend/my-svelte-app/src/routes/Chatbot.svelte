<script>
  let questionText = '';
  let answerText = '';
  let references = [];
  let isLoading = false;
  let messages = []; // 대화 내용을 저장할 배열

  async function askChatbot() {
    if (!questionText) {
      answerText = "질문을 입력해주세요.";
      return;
    }

    const currentQuestion = questionText; // 현재 질문 저장
    questionText = ''; // 입력창 비우기
    isLoading = true;

    try {
      const response = await fetch('/api/chatbot/get-answer', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          question: currentQuestion
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      // 대화 내용을 배열에 추가
      messages = [...messages, {
        question: currentQuestion,
        answer: data.answer,
        references: data.references || []
      }];
    } catch (error) {
      messages = [...messages, {
        question: currentQuestion,
        answer: `Error: ${error.message}`,
        references: []
      }];
    } finally {
      isLoading = false;
    }
  }
</script>

<div class="chat-container">
  <div class="chat-messages">
    {#each messages as message}
      <div class="message-pair">
        <div class="user-message">
          <div class="message-content">
            {message.question}
          </div>
        </div>
        <div class="bot-message">
          <div class="message-content">
            {message.answer}
          </div>
          {#if message.references.length > 0}
            <div class="references-container">
              {#each message.references as ref}
                <div class="reference-item">
                  <p class="source">출처: {ref.source}</p>
                  <p class="content">{ref.content}</p>
                </div>
              {/each}
            </div>
          {/if}
        </div>
      </div>
    {/each}
    {#if isLoading}
      <div class="loading-message">
        <div class="message-content">
          답변을 생성하고 있습니다...
        </div>
      </div>
    {/if}
  </div>

  <div class="chat-input">
    <textarea
      bind:value={questionText}
      placeholder="PDF 문서의 내용에 대해 궁금한 점을 물어보세요"
      on:keydown={(e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          askChatbot();
        }
      }}
    ></textarea>
    <button class="send-button" on:click={askChatbot} disabled={isLoading}>
      {isLoading ? '처리 중...' : '전송'}
    </button>
  </div>
</div>

<style>
.chat-container {
    display: flex;
    flex-direction: column;
    height: calc(100vh - 200px); /* 화면 높이에서 상하 여백 100px 뺀 만큼 차지 */
    background-color: #f0f2f5;
    border-radius: 8px;
    overflow: hidden;
}

.chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: 20px;
     /* 화면 높이의 50%만 차지하도록 제한 */
}

  .message-pair {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .user-message {
    display: flex;
    justify-content: flex-end;
  }

  .bot-message {
    display: flex;
    flex-direction: column; /* flex-direction을 column으로 변경 */
    align-items: flex-start;
    width: 90%; /* 전체 너비의 90% 사용 */
}

.message-content {
    max-width: 90%; /* 70%에서 90%로 증가 */
    padding: 12px 16px;
    border-radius: 20px;
    word-wrap: break-word;
}

  .user-message .message-content {
    background-color: #0084ff;
    color: white;
    margin-left: auto;
  }

  .bot-message .message-content {
    background-color: white;
    color: black;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  }

  .loading-message {
    display: flex;
    justify-content: flex-start;
  }

  .loading-message .message-content {
    background-color: #e4e6eb;
    color: #65676b;
    padding: 8px 16px;
    border-radius: 18px;
    font-size: 0.9em;
  }

  .chat-input {
    display: flex;
    gap: 12px;
    align-items: stretch; /* 세로로 늘어나게 설정 */
    background-color: white;
    padding: 20px;
    height: 22vh; /* 화면 높이의 45% 차지 */
}
textarea {
    flex: 1;
    padding: 16px 20px;
    border: 1px solid #e4e6eb;
    border-radius: 20px;
    resize: none;
    min-height: 90%; /* 부모 높이만큼 차지 */
    outline: none;
    font-family: inherit;
    font-size: 20px;
    line-height: 1.5;
}


  .send-button {
    background-color: #0084ff;
    color: white;
    border: none;
    border-radius: 20px;
    padding: 10px 20px;
    cursor: pointer;
    font-weight: 500;
    height: 44px;
  }

  .send-button:disabled {
    background-color: #e4e6eb;
    cursor: not-allowed;
  }

  .send-button:hover:not(:disabled) {
    background-color: #0073e6;
  }

  .references-container {
    width: 100%; /* 참고자료가 메시지 너비 전체를 사용하도록 설정 */
    margin-top: 8px;
    padding-top: 8px;
    border-top: 1px solid #e4e6eb;
}

  .reference-item {
    background-color: #f7f8fa;
    border-radius: 12px;
    padding: 10px;
    margin-top: 8px;
    font-size: 0.9em;
  }

  .source {
    color: #65676b;
    font-weight: 500;
    margin-bottom: 4px;
  }

  .content {
    color: #050505;
  }
</style>