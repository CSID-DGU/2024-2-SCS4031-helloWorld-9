
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from multiprocessing import Process, Manager
from routers import files, info, upload, chatbot, worker_test  # 라우터 모듈 임포트
from worker import worker


def create_app(task_queue):
    # 라우터 등록
    app = FastAPI()
    app.include_router(files.router, prefix="/api/fileserver", tags=["Files"])
    app.include_router(info.router, prefix="/api/fileserver", tags=["Info"])
    app.include_router(upload.router, prefix="/api/fileserver", tags=["Upload"],dependencies=[Depends(lambda: task_queue)],)
    app.include_router(chatbot.router, prefix="/api/chatbot", tags=["chatbot"])
    app.include_router(worker_test.router, prefix="/api/worker_test", tags=["worker_test"],dependencies=[Depends(lambda: task_queue)],)
    return app

if __name__ == "__main__":


    manager = Manager()
    task_queue = manager.Queue()
    
    # 워커 프로세스 시작
    worker_process = Process(target=worker, args=(task_queue,))
    worker_process.start()
    
    try:
        app = create_app(task_queue)
        import uvicorn
        uvicorn.run("app:create_app", host="127.0.0.1", port=8000, reload=True)
    except KeyboardInterrupt:
        worker_process.join()
        print("Worker 프로세스 종료")
    finally:
        # 서버 종료 시 워커 프로세스 종료
        task_queue.put("STOP")
        worker_process.join()
        print("Worker 프로세스 종료")
