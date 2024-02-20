# pip install jamo
from jamo import h2j, j2hcj

'''
음소, 단어는 유사도 검출 // 문장, 문단은 틀린 부분 인덱스 반환
##params
user_text : 모델에서 나온 출력 값
gt          실제 텍스트 파일
option      0 : 음소    1 : 단어    2 : 문장 / 문단

##returns
option : 0,1  -> similarity        단어의 유사도 (0 ~ 100)                                  text : 사용자 발음
option : 2    -> wrong_list_idx    틀린 단어 인덱스 리스트 (gt 기준)   -1 : 틀린 단어 없음    text_list : 사용자 음절 리스트    gt_list : 실제 음절 리스트
'''

def find_wrong_index(user_text, gt, option = 0):

    text = user_text["text"]
    wrong_list_idx = []
    similarity = 0 #단어의 유사도

    #음소일 경우
    if(option == 0):

      text = text.replace(" ", "") #한 단어로 변환
      gt = gt.replace(" ", "") #한 단어로 변환

      if(gt == text):
        similarity = 100
      else:
        similarity = calculate_similarity(gt, text)

      if(similarity > 100):
        similarity = 100

      if(similarity < 0):
        similarity = 0
        

      return similarity, text

    #단어일 경우
    elif(option == 1):
      text = text.replace(" ", "")#한 단어로 변환
      gt = gt.replace(" ", "")#한 단어로 변환

      if(gt == text):
        similarity = 100
      else:
        similarity = calculate_similarity(gt, text, 1)

      if(similarity > 100):
        similarity = 100
      
      if(similarity < 0):
        similarity = 0

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

        return wrong_list_idx, text_list, gt_list

'''
단어의 유사도를 검사하는 함수

##params
gt :         실제 정답 값
user :       사용자 텍스트 값
option :     0 : 음소   1 : 단어
##returns
similarity : 유사도 (0~100)
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
