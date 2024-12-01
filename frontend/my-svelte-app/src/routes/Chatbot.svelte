<script>
  import { onMount } from 'svelte';
  import { chatMessages } from '../store.js';
 
  let questionText = '';
  let isLoading = false;

  // 초기 높이를 22vh로 설정 (px 단위로 변환)
  let chatInputHeight = window.innerHeight * 0.22;
  let isDragging = false;
  let startHeight = chatInputHeight;
  let dragStartY = 0; // 드래그 시작 시 마우스 Y 좌표 저장
 
  // 드래그 시작 시 현재 높이와 시작 위치 저장
  function handleDragStart(e) {
    isDragging = true;
    startHeight = chatInputHeight;
    dragStartY = e.clientY; // 드래그 시작 시 마우스 Y 좌표 저장
    document.addEventListener('mousemove', handleDrag);
    document.addEventListener('mouseup', handleDragEnd);
  }
 
  // 드래그 중 높이 업데이트
  function handleDrag(e) {
  if (!isDragging) return;
  const deltaY = -(e.clientY - dragStartY); // 부호를 반대로 변경
  const newHeight = Math.max(100, Math.min(window.innerHeight * 0.5, startHeight + deltaY));
  chatInputHeight = newHeight;
}
 
  // 드래그 종료 시 이벤트 제거
  function handleDragEnd() {
    isDragging = false;
    startHeight = chatInputHeight; // 마지막 높이 저장
    document.removeEventListener('mousemove', handleDrag);
    document.removeEventListener('mouseup', handleDragEnd);
  }
 
  // window resize 이벤트에 대한 처리 추가
  onMount(() => {
    window.addEventListener('resize', () => {
      const vh = window.innerHeight * 0.22;
      if (chatInputHeight === 0) {
        chatInputHeight = vh;
      }
    });
  });
 
  async function askChatbot() {
    if (!questionText) {
      $chatMessages = [...$chatMessages, {
        question: '',
        answer: "질문을 입력해주세요.",
        references: []
      }];
      return;
    }
 
    const currentQuestion = questionText;
    questionText = '';
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
      $chatMessages = [...$chatMessages, {
        question: currentQuestion,
        answer: data.answer,
        references: data.references || []
      }];
    } catch (error) {
      $chatMessages = [...$chatMessages, {
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
    {#each $chatMessages as message}
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

  <!-- 드래그 핸들 -->
  <div 
    class="resize-handle"
    on:mousedown={handleDragStart}
  ></div>

  <div class="chat-input" style="height: {chatInputHeight}px">
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
  height: calc(100vh - 200px);
  background-color: #f0f2f5;
  border-radius: 8px;
  overflow: hidden;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
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
  flex-direction: column;
  align-items: flex-start;
  width: 90%;
}

.message-content {
  max-width: 90%;
  padding: 12px 16px;
  border-radius: 20px;
  word-wrap: break-word;
}

.user-message .message-content {
  background-color: #e07100;
  color: white;
  margin-left: auto;
  font-size: 24px;
}

.bot-message .message-content {
  background-color: white;
  color: black;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  font-size: 24px;
}

.loading-message {
  display: flex;
  justify-content: flex-start;
  font-size: 24px;
}

.loading-message .message-content {
  background-color: #e4e6eb;
  color: #65676b;
  padding: 8px 16px;
  border-radius: 18px;
}

.resize-handle {
  width: 100%;
  height: 6px;
  background: #e4e6eb;
  cursor: row-resize;
  position: relative;
}

.resize-handle:hover {
  background: #e07100;
}

.resize-handle::before {
  content: '';
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 50px;
  height: 4px;
  background: #fff;
  border-radius: 2px;
}

.chat-input {
  display: flex;
  gap: 12px;
  align-items: stretch;
  background-color: white;
  padding: 20px;
  min-height: 100px;
  transition: height 0.1s ease;
}

textarea {
  flex: 1;
  padding: 16px 20px;
  border: 1px solid #e4e6eb;
  border-radius: 20px;
  resize: none;
  height: calc(100% - 32px);
  outline: none;
  font-family: inherit;
  font-size: 24px;
  line-height: 1.5;
}

.send-button {
  background-color: #e07100;
  color: white;
  border: none;
  border-radius: 20px;
  padding: 10px 20px;
  cursor: pointer;
  font-weight: 500;
  height: 44px;
  font-size: 24px;
}

.send-button:disabled {
  background-color: #e4e6eb;
  cursor: not-allowed;
  font-size: 24px;
}

.send-button:hover:not(:disabled) {
  background-color: #e07100;
  font-size: 24px;
}

.references-container {
  width: 100%;
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid #e4e6eb;
}

.reference-item {
  background-color: #f7f8fa;
  border-radius: 12px;
  padding: 10px;
  margin-top: 8px;
  font-size: 24px;
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
