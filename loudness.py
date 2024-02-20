# pip install librosa
# pip install numpy
import librosa
import librosa.display
import numpy as np

'''
목소리의 데시벨(크기)과 분산 측정

##params
audio_path : 오디오 파일 경로

##returns
max_db :     가장 큰 소리 데시벨
var :        목소리의 분산 (일정하지 못하다는 지표)
'''

def calculate_audio_maxdB_and_var(audio_path):

  y, sr = librosa.load(audio_path, sr=3000) # y : magnitude , sr : 1초당 sample 수
  db = librosa.amplitude_to_db(y)

  #noise 제거
  # 상위 10%와 하위 10%의 인덱스 계산
  lower_bound = np.percentile(db, 10)
  upper_bound = np.percentile(db, 90)

  # 상위 10%와 하위 10%를 제외한 부분 선택
  trimmed_arr = db[(db >= lower_bound) & (db <= upper_bound)]

  mean=np.mean(trimmed_arr)

  var = np.var(trimmed_arr)

  max_db=np.max(trimmed_arr)

  normal_var = 300.0

  result_dB = (max_db + 40) * 5.0/2.0
  result_dB = int(result_dB)
  if(result_dB < 0):
    result_dB = 0
  elif(result_dB > 100):
    result_dB = 100

  result_var = 0 # 0 : 정상   -1 : 목소리가 크게 변함
  if(normal_var < var):
    result_var = -1

  return result_dB, result_var