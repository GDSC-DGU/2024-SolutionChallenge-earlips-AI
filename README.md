 <div><img src="https://capsule-render.vercel.app/api?type=waving&color=0:1FA9DC,100:D5E9AA&text=Earlips" /></div>


[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FGDSC-DGU%2F2024-SolutionChallenge-earlips-frontend&count_bg=%238B8B8B&title_bg=%231FA9DC&icon=wechat.svg&icon_color=%23E7E7E7&title=Connecting+your+ears+to+your+lips%2C+Earlips&edge_flat=false)](https://hits.seeyoufarm.com)

# 👋 introduce team member

## [Back-End & AI](/2024-SolutionChallenge-earlips-AI/README.md)

| name                                         | major          | student number   | Email                |
| -------------------------------------------- | -------------- | ------ | -------------------- |
| [SEONHO LEE](https://github.com/capableofanything)| Multi Media Engineering| 19st |retsgo01@gmail.com|
| [EUNSEO LIM](https://github.com/som0309) |Imformation Comunication Engineering| 20st |eunseolim1018@naver.com|


---

# 🛠️ Tech

## Frameworks & Stack
numpy, librosa, jamo, torch, transformers, fastapi, pydub, python-multipart, accelerate, uvicorn

## Server
google cloud platform, firebase

---

## 1. Project Name
2024 Solution Challenge

## 2. Introduce Project
The mission of the Solution Challenge is to solve for one or more of the United Nations' 17 Sustainable Development Goals using Google technology.

## 3. Project Structure


## 4. Demonstration vedio and drive screens

### 💻 Demonstration vedio

### ✨ Screen

## 5. Overall server structure


## 6. Detail server structure


## 7. Running
### Setting Up a Virtual Machine Instance
* Create a Virtual Machine instance with one GPU T4 and 2 cores, equipped with 15GB of memory. In my case, I used Google Cloud Platform.
* Machine Type: n1-standard-4
* GPU: 1 x NVIDIA Tesla T4 
* Cores: 2
* Memory: 15GB
* Operating System: Deep Learning on Linux
* OS version: Deep Learning VM with CUDA 11.8 M116 : Debian 11, Python 3.10. With CUDA 11.8 preinstalled.
### Git File Upload Server
* Set up a git file upload server on the created Virtual Machine instance.
```console
# Example command for setting up git file upload server
git init --bare my-repo.git
```
### Installing Requirements
* In the server console, run the following command to install the necessary requirements:
```console
pip install -r requirements.txt
```
* In my case, I installed only "my_install_package.txt"
### Running the Server
* Make sure to replace x.x.x.x with the desired host IP address and x with the preferred port number.
* Execute the following command to run the server:
```console
uvicorn server:app --reload --host=x.x.x.x --port=x
```
* If you encounter an FFmpeg error, resolve it by running the following command in the server console:
```console
conda install ffmpeg
```
---
## 8. OpenSource 
* AI : openai/whisper-large-v3 (Hugging Face)
