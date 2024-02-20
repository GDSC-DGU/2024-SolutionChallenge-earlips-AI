'''
in :  문단(모델에서 나온 출력 값)
out : 문장
문단을 문장으로 분리해서 리스트로 리턴해주는 함수

##params
user_text : 모델에서 나온 출력 값

##returns
sentences : 문장으로 분리한 리스트
'''

def paragraph_to_sentence_list(user_text):

  sentences = []
  num_sentence = len(user_text['chunks'])
  for i in range(num_sentence):
    sentences.append(user_text['chunks'][i]['text'])

  return sentences

#실제 정답 text용
def paragraph_to_sentence_list2(user_text):

  user_text = user_text.replace("?","@")
  user_text = user_text.replace("!","@")
  user_text = user_text.replace(".","@")
  sentences = user_text.split(sep="@")

  if("" in sentences):
    sentences.remove("")
  return sentences