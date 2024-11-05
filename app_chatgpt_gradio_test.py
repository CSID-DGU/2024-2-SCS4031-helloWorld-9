import os
from openai import OpenAI
from dotenv import load_dotenv
import gradio as gr

# .env 파일에서 환경 변수 로드
load_dotenv()

# OpenAI API 클라이언트 설정
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ChatGPT 모델을 사용하여 응답 생성
def chatbot(input_text):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": input_text}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Gradio 인터페이스 설정
interface = gr.Interface(
    fn=chatbot,
    inputs="text",
    outputs="text",
    title="Gradio 기반 ChatGPT 챗봇",
    description="OpenAI API와 Gradio를 사용한 간단한 챗봇입니다."
)

# 인터페이스 실행
if __name__ == "__main__":
    interface.launch()
