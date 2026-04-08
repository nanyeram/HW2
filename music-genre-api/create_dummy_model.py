import os
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

def create_model():
    print("🚀 파이프라인 테스트용 구조화 모델 생성을 시작합니다...")
    
    # 1. ml_service.py에서 생성하는 MFCC 특징(n_mfcc=13)과 동일한 구조의 더미 데이터 1000개 생성
    # 13개의 특징을 가지고 10종류 중 하나로 분류하는 데이터 원리
    X, y_idx = make_classification(
        n_samples=1000, 
        n_features=13, 
        n_informative=10, 
        n_classes=10, 
        random_state=42
    )
    
    # 2. 클래스 인덱스(0~9)를 장르 텍스트로 변환
    genres = ["blues", "classical", "country", "disco", "hiphop", "jazz", "metal", "pop", "reggae", "rock"]
    y = np.array([genres[i] for i in y_idx])

    # 3. 모델 정의 및 학습 (랜덤 포레스트)
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X, y)
    print("✅ 모델 피팅 완료.")

    # 4. 모델 저장
    os.makedirs("models", exist_ok=True)
    model_path = "models/genre_model.pkl"
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
        
    print(f"🎉 성공! 학습된 모델이 '{model_path}' 에 저장되었습니다.")
    print("이제 FastAPI 서버가 이 모델 파일을 읽어와서 실제 추천 엔진을 작동시킬 수 있습니다.")

if __name__ == "__main__":
    create_model()
