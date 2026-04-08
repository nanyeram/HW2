import sounddevice as sd
import numpy as np

class AudioService:
    @staticmethod
    def record_audio(duration: int = 10, sample_rate: int = 22050) -> np.ndarray:
        """
        맥북 마이크를 사용해 지정된 시간(초)만큼 오디오를 녹음합니다.
        """
        print(f"🎤 {duration}초간 마이크 녹음을 시작합니다...")
        # 마이크로부터 데이터 읽기 (모노 채널)
        recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
        sd.wait() # 녹음이 끝날 때까지 대기
        print("✅ 녹음 완료!")
        
        # librosa 등에서 처리하기 편하도록 1D array로 변환
        return recording.flatten()
