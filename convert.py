from pydub import AudioSegment
import os
from fastapi import UploadFile

def aac_to_mp3(file: UploadFile, file_name, export_path):
    # 업로드된 파일을 저장
    basic_path = os.path.dirname(os.path.abspath)
    upload_file_path = os.path.join(basic_path, file.filename)
    with open(upload_file_path, "w") as f:
        f.write(file.read())
    
    # acc파일을 AudioSegment 객체 이용해서 mp3파일로 변환
    audio = AudioSegment.from_file(upload_file_path, format="aac")
    audio.export("{}/{}.mp3".format(export_path, file_name), format="mp3")
