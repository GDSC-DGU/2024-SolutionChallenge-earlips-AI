# pip install pydub
# pip install fastapi
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
import os
from fastapi import UploadFile, HTTPException

'''
 aac파일을 mp3파일로 변환하는 함수

 ##params
 file : aac 파일 경로

 ##returns
 해당 경로에 mp3파일 생성
'''

def aac_to_mp3(file: UploadFile):

    # aac 파일 저장
    basic_path = os.path.dirname(os.path.abspath(__file__))
    upload_file_path = os.path.join(basic_path, file.filename)
    with open(upload_file_path, "wb") as f:
        f.write(file.file.read())

    expansion_name = upload_file_path.split(".")[1]
    if(expansion_name != "aac"):
        os.remove(upload_file_path)
        return HTTPException(status_code=999, detail="not aac file!")
        
    # aac파일을 mp3파일로 변환
    try:
        audio = AudioSegment.from_file(upload_file_path, format="aac")
    except CouldntDecodeError as e:
        # Check if the issue is related to a broken AAC file
        if "Error decoding" in str(e):
            os.remove(upload_file_path)
            return HTTPException(status_code=999, detail="AAC file is broken")
        else:
            # Handle other decoding errors
            os.remove(upload_file_path)
            return HTTPException(status_code=999, detail="Failed to decode audio file")
    
    #mp3 파일 저장
    temp = "temp"
    upload_mp3_path = os.path.join(basic_path, temp)
    audio.export("{}.mp3".format(upload_mp3_path), format="mp3")

    #aac 파일 삭제
    os.remove(upload_file_path)

    return upload_mp3_path