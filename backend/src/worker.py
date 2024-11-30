from multiprocessing import Queue
import logging
import time

# 로깅 설정
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger("worker")

def worker(queue: Queue):
    """
    작업 큐에서 작업을 받아 처리하는 워커 함수.
    """
    logger.info("Worker 프로세스가 시작되었습니다.") 
    while True:
        logger.info("Worker가 큐에서 작업을 기다리고 있습니다...")
        logger.info(f"Worker에서 Queue ID: {id(queue)}")
        task = queue.get() # Queue 가 블로킹 상태. 새로운 Item 이 들어올때까지 대기
        logger.info("Worker 블로킹 해제")  # 블로킹 해제 로그
        if task == "STOP":
            logger.info("Worker 종료")
            break
        logger.info(f"작업 처리 중: {task}")
        time.sleep(5)  # 작업 시뮬레이션
        logger.info(f"작업 완료: {task}")
