from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import logging
from rag_utils.embedding import Embedder  # VectorDB 초기화에 필요
from rag_utils.retrieval import Retriever  # RAG 시스템
from pathlib import Path
import time
import os
import shutil
from routers.sse import sse_message
import asyncio

logger = logging.getLogger("init_vectorDB")
logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",)

def try_init_vectorDB_from_uploads(db_path,upload_path):
    # 이미 업로드된 PDF 파일 임베딩
    try:
        logger.info("trying init vectorDB from uploads")
        embedder = Embedder(db_path)
        pdf_files = [file for file in upload_path.rglob("*.pdf") if file.is_file()]

        if not pdf_files:
            logger.info("No PDF files found.")
            # PDF 파일이 없는 경우 추가 작업
        else:
            logger.info(f"Found {len(pdf_files)} PDF files:")
            for pdf in pdf_files:
                logger.info(f"pdf 파일 임베딩 시작 : {pdf}")
                asyncio.run(sse_message(f"파일 임베딩 중입니다... : {pdf}"))
                embedder.add_docs(pdf)
                logger.info(f"pdf 파일 임베딩 완료 : {pdf}")
                asyncio.run(sse_message(f"파일 임베딩을 완료하였습니다 : {pdf}"))
                time.sleep(1) # 너무 빠른 재시도로 openai api http request 가 거절되는 문제 해결
            asyncio.run(sse_message(f"모든 파일을 임베딩을 완료하였습니다. 챗봇이 준비되었습니다."))
    except Exception as e:
        logger.error(f"Failed to gen embedder: {str(e)}")
        retriev_gen_error = e
        responser = None




def remove_vectorDB(db_path):
    # 벡터 DB 초기화: 기존 DB 삭제
    try:
        if os.path.exists(db_path):
            shutil.rmtree(db_path)
            print(f"Deleted VectorDB at {db_path}")
        else:
            print(f"No VectorDB found at {db_path}")
    except Exception as e:
        print(f"Failed to delete VectorDB: {e}")