from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from services.audio_service import AudioService
from services.ml_service import MLService
import librosa
import tempfile
import os

router = APIRouter()
ml_service = MLService()
audio_service = AudioService()

@router.get("/health")
def read_health():
    return {"status": "ok", "message": "음악 장르 분류기 API가 실행 중입니다."}

@router.post("/predict/record")
def predict_from_mic():
    """
    서버(맥북)의 마이크를 켜서 10초간 녹음한 뒤 장르를 예측합니다.
    """
    try:
        # 1. 마이크에서 10초간 녹음
        audio_data = audio_service.record_audio(duration=10)
        
        # 2. ML 모델을 통해 장르 예측
        predicted_genre = ml_service.predict_genre(audio_data)
        recommendations = ml_service.get_recommendations(predicted_genre)
        
        return {
            "status": "success",
            "source": "microphone",
            "duration": "10s",
            "predicted_genre": predicted_genre,
            "recommendations": recommendations
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

@router.post("/predict/upload")
async def predict_from_file(file: UploadFile = File(...)):
    """
    음원 파일을 업로드받아 장르를 예측합니다. (MLOps 확장을 위한 표준 API형태)
    """
    try:
        # 임시 파일로 저장하여 librosa로 읽기
        with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
            temp_audio.write(await file.read())
            temp_audio_path = temp_audio.name

        # 오디오 데이터 로드
        y, sr = librosa.load(temp_audio_path, sr=22050, duration=10.0)
        os.remove(temp_audio_path)

        # 예측
        predicted_genre = ml_service.predict_genre(y, sr)
        recommendations = ml_service.get_recommendations(predicted_genre)
        
        return {
            "status": "success",
            "source": "upload",
            "filename": file.filename,
            "predicted_genre": predicted_genre,
            "recommendations": recommendations
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})
