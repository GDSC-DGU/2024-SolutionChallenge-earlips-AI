import librosa
import numpy as np

'''
오디오 파일을 받으면, 시간에 따른 dB값을 리스트로 반환(추후 vibration의 값으로 사용)
##params
audio_path : 오디오 파일 경로
threshold : 임계값(민감도), 임계값을 넘으면 유의미한 변화라고 생각하여 진동을 다르게 줌.
frame_length : 한 프레임당 샘플의 수
hop_length : 연속적인 프레임 사이의 샘플 수

##returns
change_times_scaled : 리스트, 각 시간에 따른 값
quantized_dB : 리스트, 양자화된 1~255사이의 진동 값
'''
'''
def quantize_audio_db(audio_path, threshold=0, frame_length=2048, hop_length=512):
    # 오디오 파일 로드
    y, sr = librosa.load(audio_path, sr=3000)
    
    # 진폭을 dB로 변환 (키워드 인자로 수정)
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=frame_length, hop_length=hop_length)
    S_db = librosa.power_to_db(S, ref=np.max)
    
    # 시간 축 정보 계산
    times = librosa.frames_to_time(np.arange(S_db.shape[1]), sr=sr, hop_length=hop_length)
    
    # dB 변화 계산
    dB_changes = np.diff(S_db, axis=1)
    significant_changes = np.where(np.abs(dB_changes) > threshold)

    # 시간과 dB 변화가 큰 값 필터링
    change_times = times[significant_changes[1]]

    if len(change_times) <= 1:
        return [0], [0]
    change_dBs = dB_changes[significant_changes]
    
    # dB 변화 정규화
    min_dB, max_dB = np.min(change_dBs), np.max(change_dBs)
    normalized_dB = 1 + 254 * (change_dBs - min_dB) / (max_dB - min_dB)
    quantized_dB = normalized_dB.astype(int)
    
    # change_times 값을 1000배 하고 int 형으로 변환
    change_times_scaled = (change_times * 1000).astype(int)

    return change_times_scaled.tolist(), quantized_dB.tolist()
'''

def quantize_audio_db(audio_path, threshold=5, frame_length=2048, hop_length=512):
    import librosa
    import numpy as np
    
    # 오디오 파일 로드
    y, sr = librosa.load(audio_path, sr=None)
    
    # 진폭을 dB로 변환
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=frame_length, hop_length=hop_length)
    S_db = librosa.power_to_db(S, ref=np.max)
    
    # 시간 축 정보 계산
    times = librosa.frames_to_time(np.arange(S_db.shape[1]), sr=sr, hop_length=hop_length)
    
    # dB 변화 계산
    dB_changes = np.max(np.abs(np.diff(S_db, axis=1)), axis=0)
    significant_changes = dB_changes > threshold

    # 변화가 중요한 시점에 대해 시간 추출
    significant_times = times[:-1][significant_changes]  # 마지막 시간은 diff로 인해 하나 적습니다
    
    if len(significant_times) <= 1:
        return [0], [0]

    # 변화 시간 계산: 첫 번째 시간은 그대로, 이후 시간은 이전 시간과의 차이
    diff_times = np.diff(significant_times, prepend=significant_times[0])
    diff_times[0] = significant_times[0]
    
    # dB 변화 정규화
    significant_dBs = dB_changes[significant_changes]
    min_dB, max_dB = np.min(significant_dBs), np.max(significant_dBs)
    normalized_dB = 1 + 254 * (significant_dBs - min_dB) / (max_dB - min_dB)
    quantized_dB = normalized_dB.astype(int)
    # diff_times 값을 1000배 하고 int 형으로 변환
    diff_times = (diff_times * 1000).astype(int)
    return diff_times.tolist(), quantized_dB.tolist()

'''
# 예시 사용법
times, dbs = quantize_audio_db(audio_path)
print("Times of significant changes:", times)
print("Quantized dB values:", dbs)
'''