import os
from openai import OpenAI
from dotenv import load_dotenv
import gradio as gr
import pdfplumber
from typing import List
import tempfile
import shutil

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class PDFManager:
    def __init__(self):
        self.pdf_contents = {}
        self.temp_dir = tempfile.mkdtemp()
        
    def process_pdf(self, files: List[tempfile._TemporaryFileWrapper]) -> tuple:
        """Process multiple PDF files and store their contents"""
        if not files:
            return "파일을 선택해주세요.", None
            
        new_files = []
        for file in files:
            temp_path = os.path.join(self.temp_dir, os.path.basename(file.name))
            shutil.copy2(file.name, temp_path)
            
            if temp_path not in self.pdf_contents:
                try:
                    with pdfplumber.open(temp_path) as pdf:
                        content = ""
                        for page in pdf.pages:
                            content += page.extract_text() + "\n"
                        self.pdf_contents[temp_path] = {
                            'content': content,
                            'filename': os.path.basename(file.name)
                        }
                        new_files.append(os.path.basename(file.name))
                except Exception as e:
                    return f"Error processing {os.path.basename(file.name)}: {str(e)}", None
        
        if new_files:
            return f"성공적으로 처리된 파일: {', '.join(new_files)}", None
        return "이미 업로드된 파일입니다.", None
    
    def remove_pdf(self, filename: str) -> str:
        for path, info in list(self.pdf_contents.items()):
            if info['filename'] == filename:
                del self.pdf_contents[path]
                if os.path.exists(path):
                    os.remove(path)
                return f"{filename} 파일이 삭제되었습니다."
        return f"{filename} 파일을 찾을 수 없습니다."
    
    def get_all_content(self) -> str:
        return "\n\n=====\n\n".join(info['content'] for info in self.pdf_contents.values())
    
    def get_loaded_files(self) -> List[str]:
        return [info['filename'] for info in self.pdf_contents.values()]

pdf_manager = PDFManager()

def chatbot(input_text: str) -> str:
    try:
        pdf_content = pdf_manager.get_all_content()
        if not pdf_content:
            return "먼저 PDF 파일을 업로드해주세요."
        
        full_input = f"다음 PDF 문서들의 내용을 바탕으로 질문에 답변해주세요:\n\n{pdf_content}\n\n질문: {input_text}"
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": full_input}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def update_file_list() -> str:
    files = pdf_manager.get_loaded_files()
    if not files:
        return "로드된 파일이 없습니다."
    return "\n".join([f"- {f}" for f in files])

def remove_selected_file(filename: str) -> tuple:
    result = pdf_manager.remove_pdf(filename)
    return result, update_file_list(), gr.Dropdown(choices=pdf_manager.get_loaded_files())

def process_and_update(files):
    status, _ = pdf_manager.process_pdf(files)
    files_list = update_file_list()
    new_dropdown = gr.Dropdown(choices=pdf_manager.get_loaded_files())
    return status, files_list, new_dropdown, None

with gr.Blocks() as interface:
    gr.Markdown("# 보험 문서 챗봇 검색 시스템")
    
    with gr.Tabs():
        with gr.Tab("PDF 관리"):
            with gr.Row():
                with gr.Column():
                    # File upload section
                    file_input = gr.File(
                        label="PDF 파일 업로드",
                        file_count="multiple",
                        type="filepath"
                    )
                    upload_status = gr.Textbox(label="업로드 상태", interactive=False)
                
                with gr.Column():
                    gr.Markdown("### PDF 파일 삭제")
                    file_dropdown = gr.Dropdown(
                        choices=pdf_manager.get_loaded_files(),
                        label="삭제할 파일 선택",
                        interactive=True
                    )
                    remove_button = gr.Button("선택한 파일 삭제")
            
            gr.Markdown("### 현재 로드된 PDF 파일들")
            loaded_files = gr.Textbox(
                label="로드된 파일 목록",
                value=update_file_list(),
                interactive=False
            )
            
            file_input.upload(
                fn=process_and_update,
                inputs=[file_input],
                outputs=[
                    upload_status,
                    loaded_files,
                    file_dropdown,
                    file_input
                ]
            )
            
            remove_button.click(
                fn=remove_selected_file,
                inputs=[file_dropdown],
                outputs=[upload_status, loaded_files, file_dropdown]
            )
            
        with gr.Tab("챗봇"):
            question = gr.Textbox(
                label="질문을 입력하세요",
                placeholder="궁금한 점을 물어보세요"
            )
            answer = gr.Textbox(label="답변", interactive=False)
            ask_button = gr.Button("질문하기")
            ask_button.click(chatbot, inputs=[question], outputs=[answer])

if __name__ == "__main__":
    interface.launch()