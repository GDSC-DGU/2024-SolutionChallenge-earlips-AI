# pip install torch
# pip install pydub
# pip install --upgrade pip
# pip install --upgrade git+https://github.com/huggingface/transformers.git
from fastapi import FastAPI, File, UploadFile
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from pydub import AudioSegment

'''
Hugging Face에 있는 openai / whisper-large-v3 사용
'''

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

'''
음성을 텍스트로 바꿔주는 함수

##params
audio_path : 음성 파일 경로

##returns
text :       음성 파일을 텍스트로 변환한 결과
'''

def speech_to_text(audio_path):
    result = pipe(audio_path, return_timestamps = True ,generate_kwargs={"language" : "korean"})
    return result

def speech_to_text_english(audio_path):
    result = pipe(audio_path, return_timestamps = True ,generate_kwargs={"language" : "english"})
    return result