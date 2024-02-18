from fastapi import FastAPI, File, UploadFile
import uvicorn
#서버 올리기
app = FastAPI()

#음절 교정
@app.post("/study/syllable")
async def syllable(syll: str, file: UploadFile = File(...)):
    #녹음 파일 객체
    audio = file.file
    #녹음 파일 변환
    #녹음 파일 처리
    result: str
    return result

#단어 교정
@app.post("/study/word")
async def word(word: str, file: UploadFile = File(...)):
    #녹음 파일 객체
    audio = file.file
    #녹음 파일 변환
    #녹음 파일 처리
    result: str
    return result

#문장 교정
@app.post("/study/sentence")
async def sentence(sen: str, file: UploadFile = File(...)):
    #녹음 파일 객체
    audio = file.file
    #녹음 파일 변환
    #녹음 파일 처리
    result: str
    return result

#문단 교정
@app.post("/study/paragraph")
async def paragraph(para: str, file: UploadFile = File(...)):
    #녹음 파일 객체
    audio = file.file
    #녹음 파일 변환
    #녹음 파일 처리
    result: str
    return result

#대본 학습
@app.post("/script")
async def script(scr: str, file: UploadFile = File(...)):
    #녹음 파일 객체
    audio = file.file
    #녹음 파일 변환
    #녹음 파일 처리
    result: str
    return result

#실시간 발음 테스트
@app.post("/real_time")
async def script(file: UploadFile = File(...)):
    #녹음 파일 객체
    audio = file.file
    #녹음 파일 변환
    #녹음 파일 처리
    result: str
    return result