from fastapi import FastAPI, File, UploadFile

# 서버 올리기
app = FastAPI()

# 음절 교정
@app.post("/study/syllable")
async def syllable(syll: str, file: UploadFile = File(...)):

    # 녹음 파일 객체
    name = file.filename
    sep_name = name.split(".")

    aac_to_mp3(file, sep_name[0], "/mp3/")

    audio_path = "/mp3/{}.mp3".format(sep_name[0])

    #모델에 넣어준다.
    result = speech_to_text(audio_path)

    #틀린거 찾기
    similarity, user_text = find_wrong_index(result, syll, option=0)#유사도, 사용자 발음

    dic = {"pronunciation" : user_text, "similarity" : similarity }

    #서버에 올라간 데이터 삭제하기.

    return dic


# 단어 교정
@app.post("/study/word")
async def word(word: str, file: UploadFile = File(...)):

    # 녹음 파일 객체
    name = file.filename
    sep_name = name.split(".")

    aac_to_mp3(file, sep_name[0], "/mp3/")

    audio_path = "/mp3/{}.mp3".format(sep_name[0])

    # 모델에 넣어준다.
    result = speech_to_text(audio_path)

    # 틀린거 찾기
    similarity, user_text = find_wrong_index(result, syll, option=1)  # 유사도, 사용자 발음

    dic = {"pronunciation" : user_text, "similarity" : similarity }

    # 서버에 올라간 데이터 삭제하기.

    return dic


# 문장 교정
@app.post("/study/sentence")
async def sentence(sen: str, file: UploadFile = File(...)):

    # 녹음 파일 객체
    name = file.filename
    sep_name = name.split(".")

    aac_to_mp3(file, sep_name[0], "/mp3/")

    audio_path = "/mp3/{}.mp3".format(sep_name[0])

    # 모델에 넣어준다.
    result = speech_to_text(audio_path)

    # 틀린거 찾기
    wrong_list_idx, user_word_list, gt_word_list = find_wrong_index(result, syll, option=2)  # 틀린 단어 인덱스 리스트, 사용자 단어 리스트, 정답 값 단어 리스트
    db, var = calculate_audio_maxdB_and_var(audio_path) #목소리 크기(0~100), var(1 or -1)
    speed = compare_speed(result, sen, option = 0) #speed(0, 0.5, 1, 1.5, 2)

    dic = {"sentence_word" : gt_word_list, "user_word" : user_word_list, "wrong" : wrong_list_idx, "loudness" : db, "variance" : var, "speed" : speed}

    #서버 올린 데이터 삭제하기.

    return dic


# 문단 교정
@app.post("/study/paragraph")
async def paragraph(para: str, file: UploadFile = File(...)):

    # 녹음 파일 객체
    name = file.filename
    sep_name = name.split(".")

    aac_to_mp3(file, sep_name[0], "/mp3/")

    audio_path = "/mp3/{}.mp3".format(sep_name[0])

    # 모델에 넣어준다.
    result = speech_to_text(audio_path)

    wrong_list_idx, user_word_list, gt_word_list = find_wrong_index(result, para, option = 2)  # 틀린 단어 인덱스 리스트, 사용자 단어 리스트, 정답 값 단어 리스트
    paragraph_sentence = paragraph_to_sentence_list2(para)
    user_sentence = paragraph_to_sentence_list2(result)
    speed = compare_speed(result, para, option = 1)

    dic = {"paragraph_word": gt_word_list, "user_word": user_word_list, "paragraph_sentence": paragraph_sentence, "user_sentence": user_sentence, "wrong": wrong_list_idx, "speed": speed}

    # 서버 올린 데이터 삭제하기

    return dic


# 대본 학습
@app.post("/script")
async def script(scr: str, file: UploadFile = File(...)):
    # 녹음 파일 객체
    name = file.filename
    sep_name = name.split(".")

    aac_to_mp3(file, sep_name[0], "/mp3/")

    audio_path = "/mp3/{}.mp3".format(sep_name[0])

    # 모델에 넣어준다.
    result = speech_to_text(audio_path)

    wrong_list_idx, user_word_list, gt_word_list = find_wrong_index(result, para,
                                                                    option=2)  # 틀린 단어 인덱스 리스트, 사용자 단어 리스트, 정답 값 단어 리스트
    paragraph_sentence = paragraph_to_sentence_list2(para)
    user_sentence = paragraph_to_sentence_list2(result)
    speed = compare_speed(result, para, option=1)

    dic = {"paragraph_word": gt_word_list, "user_word": user_word_list, "paragraph_sentence": paragraph_sentence, "user_sentence": user_sentence, "wrong": wrong_list_idx, "speed": speed}

    # 서버 올린 데이터 삭제하기

    return dic


# 실시간 발음 테스트
@app.post("/real_time")
async def script(file: UploadFile = File(...)):

    # 녹음 파일 객체
    name = file.filename
    sep_name = name.split(".")

    aac_to_mp3(file, sep_name[0], "/mp3/")

    audio_path = "/mp3/{}.mp3".format(sep_name[0])

    # 모델에 넣어준다.
    result = speech_to_text(audio_path)

    dic = {"user_total" : result['text']}

    # 서버 올린 데이터 삭제하기

    return dic


#pip install --upgrade pip
#pip install --upgrade git+https://github.com/huggingface/transformers.git

import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model_id = "openai/whisper-large-v3"


model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
)
model.to(device)

processor = AutoProcessor.from_pretrained(model_id)

pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    max_new_tokens=128,
    chunk_length_s=30,
    batch_size=16,
    return_timestamps=True,
    torch_dtype=torch_dtype,
    device=device,
)
######################################################################################################################################################################
#pip install jamo
from jamo import h2j, j2hcj
'''
음성을 텍스트로 바꿔주는 함수

##params
audio_path : 음성 파일 경로

##returns
text : 음성 파일을 텍스트로 변환한 결과
'''
def speech_to_text(audio_path):
  result = pipe(audio_path, return_timestamps = True ,generate_kwargs={"language" : "korean"})
  return result
######################################################################################################################################################################
'''
in : 문단(모델에서 나온 출력 값)
out : 문장
각 문장을 리스트로 리턴해주는 함수

##params
user_text : 모델에서 나온 출력 값

##returns
sentences : 문장 리스트
'''
def paragraph_to_sentence_list(user_text):

  sentences = []
  num_sentence = len(user_text['chunks'])
  for i in range(num_sentence):
    sentences.append(user_text['chunks'][i]['text'])

  return sentences

#더 정확함
def paragraph_to_sentence_list2(user_text):

  user_text['text'] = user_text['text'].replace("?","@")
  user_text['text'] = user_text['text'].replace("!","@")
  user_text['text'] = user_text['text'].replace(".","@")
  sentences = user_text['text'].split(sep="@")
  sentences.remove("")
  return sentences
######################################################################################################################################################################
'''
음소, 단어는 유사도 검출 // 문장, 문단은 틀린 인덱스 반환
##params
user_text            모델에서 나온 출력 값
gt                   실제 텍스트 파일
option               0 : 음소   1 : 단어   2 : 문장 / 문단

##returns
option : 0,1  -> similarity           단어의 유사도(0 ~ 100)                                         text : 사용자 발음
option : 2  -> wrong_list_idx         틀린 단어의 인덱스 리스트(gt 기준)   -1 : 틀린 단어가 없음          text_list : 사용자 음절 리스트    gt_list : 실제 음절 리스트
'''
def find_wrong_index(user_text, gt, option = 0):

    text = user_text["text"]
    wrong_list_idx = []
    similarity = 0 #단어의 유사도

    #음소일 경우
    if(option == 0):

      text = text.replace(" ", "")#한 단어로 변환
      gt = gt.replace(" ", "")#한 단어로 변환

      if(gt == text):
        similarity = 100


      else:
        similarity = calculate_similarity(gt, text)

      return similarity, text

    #단어일 경우
    elif(option == 1):
      text = text.replace(" ", "")#한 단어로 변환
      gt = gt.replace(" ", "")#한 단어로 변환

      if(gt == text):
        similarity = 100


      else:
        similarity = calculate_similarity(gt, text, 1)

      return similarity, text

    #문장일 경우(두 단어 이상)
    elif(option == 2):

      #전처리 : '?', '!'는 인식 가능 <-> ',', '.'는 사람마다 다를 수 있으므로 제거함
      text = text.replace(",","")
      text = text.replace(".","")

      gt = gt.replace(",","")
      gt = gt.replace(".","")

      text_list = text.split()
      gt_list = gt.split()

      #text_list와 gt_list의 길이가 같을 경우
      if(len(text_list) == len(gt_list)):
        for i in range(len(text_list)):
          if(text_list[i] != gt_list[i]):
            wrong_list_idx.append(i)

        if(len(wrong_list_idx) == 0):
          wrong_list_idx.append(-1)

        return wrong_list_idx, text_list, gt_list

      #text_list와 gt_list의 길이가 다를 경우 : text_list > gt_list
      elif(len(text_list) > len(gt_list)):
        for i in range(len(gt_list)):
          #틀린 부분 찾기
          if(text_list[i] != gt_list[i]):
            wrong_list_idx.append(i)

        #개수 넘어간 부분 찾기
        diff = len(text_list) - len(gt_list)
        for i in range(diff):
          wrong_list_idx.append(i+len(gt_list))

        return wrong_list_idx, text_list, gt_list

      #text_list와 gt_list의 길이가 다를 경우
      elif(len(text_list) < len(gt_list)):
        for i in range(len(text_list)):
          #틀린 부분 찾기
          if(text_list[i] != gt_list[i]):
            wrong_list_idx.append(i)

        #개수 넘어간 부분 찾기
        diff = len(gt_list) - len(text_list)
        for i in range(diff):
          wrong_list_idx.append(i+len(text_list))

        return wrong_list_idx, text_list, gt_list

'''
단어의 유사도를 검사하는 함수

##params
gt :        실제 정답 값
user :      사용자 텍스트 값
option :    0 : 음소   1 : 단어
##returns
int :       유사도(0~100)
'''
def calculate_similarity(gt, user, option = 0):

  similarity = 0

  if(gt == user):
    similarity = 100
    return similarity
  else:
    sep_gt = j2hcj(h2j(gt))
    sep_user = j2hcj(h2j(user))

    len_sep_gt = len(sep_gt)
    len_sep_user = len(sep_user)

    if(len_sep_gt==len_sep_user):
      for i in range(len_sep_gt):
        if(sep_gt[i]==sep_user[i]):
          similarity += 33

    elif(len_sep_gt>len_sep_user):
      for i in range(len_sep_user):
        if(sep_gt[i]==sep_user[i]):
          similarity += 33

    else:
      for i in range(len_sep_gt):
        if(sep_gt[i]==sep_user[i]):
          similarity += 33

    if(option == 1):
      len_gt = len(gt)
      len_user = len(user)
      if(len_gt>len_user):
        similarity = similarity//len_gt
      else:
        similarity = similarity//len_user

    return similarity
######################################################################################################################################################################
'''
사용자의 말하기 속도를 측정하는 함수
##params
user_timestamp : 모델에서 나온 출력 값
text : 사용자의 텍스트
option : 0 : 문장 1 : 문단

##returns
0 : 매우 느림
0.5 : 느림
1 : 적당함
1.5 : 빠름
2 : 매우 빠름
'''
def compare_speed(user_timestamp, text, option = 0):

  if(option == 0):
    timestamp = user_timestamp['chunks'][0]['timestamp']# 튜플 형태 ()
    length = len(user_timestamp['text'])
    user_speed = timestamp[1]/length
    print(user_speed)
    return check_speed(user_speed)

  elif(option == 1):
    num_text = len(user_timestamp['chunks'])

    sentence_speed = []#i 번째 문장의 속도

    for i in range(num_text):
      timestamp = user_timestamp['chunks'][i]['timestamp']
      length = len(user_timestamp['chunks'][i]['text'])
      user_speed = timestamp[1]/length
      sentence_speed.append(check_speed(user_speed))

    return sentence_speed

'''
##params
user_speed : 사용자의 말하기 속도

##returns
0 : 매우 느림
0.5 : 느림
1 : 적당함
1.5 : 빠름
2 : 매우 빠름
'''
def check_speed(user_speed):

  very_slow = 1.0 #return 0
  little_slow = (0.5, 1.0) #return 0.5
  basic = (0.1, 0.5) #return 1
  little_fast = (0.05, 0.1) #return 1.5
  very_fast = 0.05 #return 2.0

  result = 0.0

  if(very_slow <= user_speed):
    result = 0
  elif(little_slow[0] <= user_speed < little_slow[1]):
    result = 0.5
  elif(basic[0] <= user_speed < basic[1]):
    result = 1.0
  elif(little_fast[0] <= user_speed < little_fast[1]):
    result = 1.5
  elif(user_speed <= very_fast):
    result = 2.0

  return result
######################################################################################################################################################################
import librosa
import librosa.display
import numpy as np
'''
목소리의 데시벨(크기)과 분산을 측정한다.

##params
audio_path : 오디오 파일 경로

##returns
max_db :    가장 큰 소리 데시벨
var :       목소리의 분산 (일정하지 못하다는 지표)
'''
def calculate_audio_maxdB_and_var(audio_path):

  y, sr = librosa.load(audio_path, sr=3000) # y : magnitude , sr : 1초당 sample 수
  db = librosa.amplitude_to_db(y)

  #noise 제거
  # 상위 10%와 하위 10%의 인덱스를 계산합니다.
  lower_bound = np.percentile(db, 10)
  upper_bound = np.percentile(db, 90)

  # 상위 10%와 하위 10%를 제외한 부분을 선택합니다.
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
######################################################################################################################################################################
import os
'''
 aac to mp3 변환 함수

 ##params
 file :             aac 파일 경로
 file_name :        저장할 파일 이름
 export_path :      저장 위치

 ##returns
 해당 경로에 파일 생성
'''
def aac_to_mp3(file: UploadFile, file_name, export_path):

    # 업로드된 파일을 저장
    basic_path = os.path.dirname(os.path.abspath(__file__))
    upload_file_path = os.path.join(basic_path, file.filename)
    with open(upload_file_path, "wb") as f:
        f.write(file.file.read())

    # acc파일을 AudioSegment 객체 이용해서 mp3파일로 변환
    audio = AudioSegment.from_file(upload_file_path, format="aac")
    audio.export("{}/{}.mp3".format(export_path, file_name), format="mp3")