'''
사용자가 말하는 속도를 측정하는 함수
##params
user_timestamp : 모델에서 나온 출력 값
text :           사용자의 텍스트
option :         0 : 문장    1 : 문단

##returns
sentence_speed : 말하는 속도
0 : 매우 느림
0.5 : 느림
1 : 적당함
1.5 : 빠름
2 : 매우 빠름
'''

def compare_speed(user_timestamp, text, option = 0):

  if(option == 0):
    timestamp = user_timestamp['chunks'][0]['timestamp'] # 튜플 형태 ()
    length = len(user_timestamp['text'])
    user_speed = timestamp[1]/length
    print(user_speed)
    return check_speed(user_speed)

  elif(option == 1):
    num_text = len(user_timestamp['chunks'])

    sentence_speed = [] #i 번째 문장의 속도

    for i in range(num_text):
      timestamp = user_timestamp['chunks'][i]['timestamp']
      length = len(user_timestamp['chunks'][i]['text'])
      user_speed = timestamp[1]/length
      sentence_speed.append(check_speed(user_speed))

    return sentence_speed

'''
##params
user_speed : 사용자가 말하는 속도

##returns
result: 말하는 속도
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