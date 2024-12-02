import os
from glob import glob
from config import DB_PATH

def get_all_pdfs(path):
    """
    주어진 경로에서 모든 PDF 파일을 검색하여 반환하는 함수.

    :param path: 검색할 디렉터리 경로
    :return: PDF 파일 경로 리스트
    """
    # 절대 경로 변환
    absolute_path = os.path.abspath(path)
    
    # 파일 패턴 생성
    pdf_pattern = os.path.join(absolute_path, "*.pdf")
    
    # PDF 파일 리스트 반환
    pdf_files = glob(pdf_pattern)
    return pdf_files
