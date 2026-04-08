import librosa
import numpy as np
import pickle
import os

class MLService:
    def __init__(self):
        # 실제 환경에서는 학습된 .pkl 파일을 불러옵니다.
        # 여기서는 모델 파일이 없으면 더미 랜덤 예측을 하도록 예외 처리했습니다.
        self.model_path = "models/genre_model.pkl"
        self.genres = ["blues", "classical", "country", "disco", "hiphop", "jazz", "metal", "pop", "reggae", "rock"]
        
        try:
            if os.path.exists(self.model_path):
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
            else:
                self.model = None
                print("⚠️ 경고: 학습된 모델 파일이 없습니다. 더미 예측 모드로 동작합니다.")
        except Exception as e:
            print(f"모델 로드 에러: {e}")
            self.model = None

    def extract_features(self, y: np.ndarray, sr: int = 22050):
        """librosa를 활용해 MFCC 특징을 추출합니다."""
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfccs_mean = np.mean(mfccs.T, axis=0)
        return mfccs_mean

    def predict_genre(self, audio_data: np.ndarray, sr: int = 22050) -> str:
        """오디오 데이터를 받아 장르를 예측합니다."""
        features = self.extract_features(audio_data, sr)
        
        if self.model is None:
            # 모델이 없을 경우 임의의 장르 반환 (마이크 연동 테스트 용도)
            return str(np.random.choice(self.genres))
            
        # 모델 추론 (scikit-learn 사용 가정)
        # features를 2D 배열로 변환
        prediction = self.model.predict([features])
        return str(prediction[0])
