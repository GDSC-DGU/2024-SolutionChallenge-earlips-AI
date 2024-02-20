from fastapi import FastAPI, File, UploadFile, Form
import main
import os
from typing import Annotated

# 서버 올리기
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# 음절 교정
@app.post("/study/syllable")
async def syllable(audio : Annotated[UploadFile, Form()], content : Annotated[str, Form()]):

    syll = content
    file = audio

    audio_path = main.aac_to_mp3(file)
    audio_path = audio_path + ".mp3"

    #모델에 넣어준다.
    result = main.speech_to_text(audio_path)

    #틀린거 찾기
    similarity, user_text = main.find_wrong_index(result, syll, option=0)#유사도, 사용자 발음

    dic = {"pronunciation" : user_text, "similarity" : similarity }

    #서버에 올라간 데이터 삭제하기.
    os.remove(audio_path)
    return dic


# 단어 교정
@app.post("/study/word")
async def word(audio : Annotated[UploadFile, Form()], content : Annotated[str, Form()]):

    word = content
    file = audio

    audio_path = main.aac_to_mp3(file)
    audio_path = audio_path + ".mp3"

    # 모델에 넣어준다.
    result = main.speech_to_text(audio_path)

    # 틀린거 찾기
    similarity, user_text = main.find_wrong_index(result, word, option=1)  # 유사도, 사용자 발음

    dic = {"pronunciation" : user_text, "similarity" : similarity }

    # 서버에 올라간 데이터 삭제하기.
    os.remove(audio_path)

    return dic


# 문장 교정
@app.post("/study/sentence")
async def sentence(audio : Annotated[UploadFile, Form()], content : Annotated[str, Form()]):

    sen = content
    file = audio

    audio_path = main.aac_to_mp3(file)
    audio_path = audio_path + ".mp3"

    # 모델에 넣어준다.
    result = main.speech_to_text(audio_path)

    # 틀린거 찾기
    wrong_list_idx, user_word_list, gt_word_list = main.find_wrong_index(result, sen, option=2)  # 틀린 단어 인덱스 리스트, 사용자 단어 리스트, 정답 값 단어 리스트
    db, var = main.calculate_audio_maxdB_and_var(audio_path) #목소리 크기(0~100), var(1 or -1)
    speed = main.compare_speed(result, sen, option = 0) #speed(0, 0.5, 1, 1.5, 2)

    dic = {"sentence_word" : gt_word_list, "user_word" : user_word_list, "wrong" : wrong_list_idx, "loudness" : db, "variance" : var, "speed" : speed}

    #서버 올린 데이터 삭제하기.
    os.remove(audio_path)

    return dic


# 문단 교정
@app.post("/study/paragraph")
async def paragraph(audio : Annotated[UploadFile, Form()], content : Annotated[str, Form()]):

    para = content
    file = audio

    audio_path = main.aac_to_mp3(file)
    audio_path = audio_path + ".mp3"

    # 모델에 넣어준다.
    result = main.speech_to_text(audio_path)

    #예외 처리 (단어 이하가 들어올 경우) #문단이 아닌 문장일 경우 예외가 발생하는가?
    user_text = result['text']
    user_text_list = user_text.split()
    num_user_text_list = len(user_text_list)
    if(num_user_text_list <= 1):
        raise HTTPException(status_code=400, detail="User input should contain more than 1 word.")

    wrong_list_idx, user_word_list, gt_word_list = main.find_wrong_index(result, para, option = 2)  # 틀린 단어 인덱스 리스트, 사용자 단어 리스트, 정답 값 단어 리스트
    paragraph_sentence = main.paragraph_to_sentence_list(para)
    user_sentence = main.paragraph_to_sentence_list(result)
    speed = main.compare_speed(result, para, option = 1)

    dic = {"paragraph_word": gt_word_list, "user_word": user_word_list, "paragraph_sentence": paragraph_sentence, "user_sentence": user_sentence, "wrong": wrong_list_idx, "speed": speed}

    # 서버 올린 데이터 삭제하기
    os.remove(audio_path)

    return dic


# 대본 학습
@app.post("/script")
async def script(audio : Annotated[UploadFile, Form()], content : Annotated[str, Form()]):

    scr = content
    file = audio

    audio_path = main.aac_to_mp3(file)
    audio_path = audio_path + ".mp3"

    # 모델에 넣어준다.
    result = main.speech_to_text(audio_path)

    wrong_list_idx, user_word_list, gt_word_list = main.find_wrong_index(result, scr,
                                                                    option=2)  # 틀린 단어 인덱스 리스트, 사용자 단어 리스트, 정답 값 단어 리스트
    paragraph_sentence = main.paragraph_to_sentence_list(scr)
    user_sentence = main.paragraph_to_sentence_list(result)
    speed = main.compare_speed(result, scr, option=1)

    dic = {"paragraph_word": gt_word_list, "user_word": user_word_list, "paragraph_sentence": paragraph_sentence, "user_sentence": user_sentence, "wrong": wrong_list_idx, "speed": speed}

    # 서버 올린 데이터 삭제하기
    os.remove(audio_path)

    return dic


# 실시간 발음 테스트
@app.post("/real_time")
async def script(audio : Annotated[UploadFile, Form()]):

    file = audio

    audio_path = main.aac_to_mp3(file)
    audio_path = audio_path + ".mp3"

    # 모델에 넣어준다.
    result = main.speech_to_text(audio_path)

    dic = {"user_total" : result['text']}

    # 서버 올린 데이터 삭제하기
    os.remove(audio_path)

    return dic

