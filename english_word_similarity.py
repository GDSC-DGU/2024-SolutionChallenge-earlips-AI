'''
영어 음소의 바이너리 True False 확인

##params
user_text : 모델에서 나온 출력 값
gt          실제 텍스트 파일

##returns
score : 0 틀림, 1 맞춤
'''

def binary_TF_english_phoneme(user_text, gt):

    text = user.replace(" ", "") #한 단어로 변환
    gt = gt.replace(" ", "") #한 단어로 변환

    score = 0
    user = user_text["text"]
    pronunciation = user_text["text"]
    if len(user) > 1 or user != gt:
      return score, pronunciation #틀림

    score = 1
    return score, pronunciation #맞음




'''
영어 단어의 유사도 점수 반환

##params
user_text : 모델에서 나온 출력 값
gt          실제 텍스트 파일

##returns
score : 단어의 유사도 값
'''

def english_word_similarity_score(user_text, gt):

    user = user_text["text"]

    user = user.replace(" ", "")#한 단어로 변환
    gt = gt.replace(" ", "")#한 단어로 변환
    user = user.lower()#소문자로 변환 예외처리
    gt = gt.lower()
    # 영어 모음 정의
    vowels = 'aeiouAEIOU'
    # 오류 수를 저장할 리스트
    consonant_errors = 0
    vowel_errors = 0

    # 두 문자열의 길이가 다른 경우, 가장 짧은 길이로 비교를 제한
    length = min(len(user), len(gt))

    # 한 글자씩 비교
    for i in range(length):
        if user[i] != gt[i]:
            # 현재 문자가 모음인지 자음인지 판별
            if gt[i] in vowels:
                vowel_errors += 1
            else:
                consonant_errors += 1

    # 길이가 다를 경우, 더 긴 문자열의 남은 부분을 오류로 계산
    # 남은 부분의 모든 문자는 자음으로 가정
    additional_errors = abs(len(user) - len(gt))
    consonant_errors += additional_errors

    gt_length = len(gt)
    score = 100
    score = score - consonant_errors * 20
    score = score - vowel_errors * 40
    if score < 0:
      score = 0
    return score, user

'''
# 사용 예
user_input = "hallo"
correct_answer = "hello"
score =  english_word_similarity_score(user_input, correct_answer)
'''