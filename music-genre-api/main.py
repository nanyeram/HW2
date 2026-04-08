from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from api.routes import router

app = FastAPI(
    title="음악 장르 분류 API (MLOps Base)",
    description="맥북 마이크를 활용하거나 오디오 파일을 업로드하여 장르를 판별하는 간단한 API 서버",
    version="1.0.0"
)

# 정적 파일 경로 마운트 (UI 에셋용)
app.mount("/static", StaticFiles(directory="static"), name="static")

# API 라우터 등록
app.include_router(router, prefix="/api/v1")

# 루트 경로 접속 시 UI 파일 반환
@app.get("/")
async def root():
    return FileResponse("static/index.html")

if __name__ == "__main__":
    import uvicorn
    # 터미널에서 `python main.py`로 직접 실행할 때 사용됩니다.
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
