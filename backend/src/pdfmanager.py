import os
import pdfplumber
from typing import List
import tempfile
import shutil

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
            temp_path = os.path.join(self.temp_dir, os.path.basename(file.filename))
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

# import os
# import pdfplumber
# from typing import List
# import tempfile
# from fastapi import UploadFile

# class PDFManager:
#     def __init__(self):
#         self.pdf_contents = {}
#         self.temp_dir = tempfile.mkdtemp()  # 임시 디렉터리 생성

#     async def process_pdf(self, files: List[UploadFile]) -> tuple:
#         """Process multiple PDF files and store their contents"""
#         if not files:
#             return "파일을 선택해주세요.", None

#         new_files = []
#         for file in files:
#             # 임시 파일 저장
#             temp_path = os.path.join(self.temp_dir, file.filename)
#             with open(temp_path, "wb") as temp_file:
#                 temp_file.write(await file.read())  # UploadFile 객체의 데이터를 읽어 씀

#             # 파일 중복 검사
#             if temp_path not in self.pdf_contents:
#                 try:
#                     with pdfplumber.open(temp_path) as pdf:
#                         content = ""
#                         for page in pdf.pages:
#                             text = page.extract_text()
#                             if text:  # 페이지에 텍스트가 있는지 확인
#                                 content += text + "\n"
#                         self.pdf_contents[temp_path] = {
#                             'content': content.strip(),
#                             'filename': file.filename
#                         }
#                         new_files.append(file.filename)
#                 except Exception as e:
#                     return f"Error processing {file.filename}: {str(e)}", None

#         if new_files:
#             return f"성공적으로 처리된 파일: {', '.join(new_files)}", None
#         return "이미 업로드된 파일입니다.", None

#     def remove_pdf(self, filename: str) -> str:
#         for path, info in list(self.pdf_contents.items()):
#             if info['filename'] == filename:
#                 del self.pdf_contents[path]
#                 if os.path.exists(path):
#                     os.remove(path)
#                 return f"{filename} 파일이 삭제되었습니다."
#         return f"{filename} 파일을 찾을 수 없습니다."

#     def get_all_content(self) -> str:
#         return "\n\n=====\n\n".join(info['content'] for info in self.pdf_contents.values())

#     def get_loaded_files(self) -> List[str]:
#         return [info['filename'] for info in self.pdf_contents.values()]
