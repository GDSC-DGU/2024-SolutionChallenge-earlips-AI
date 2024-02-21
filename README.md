# OpenSource 
* openai/whisper-large-v3 (Hugging Face)
# Setting Up a Virtual Machine Instance
* Create a Virtual Machine instance with one GPU T4 and 3 cores, equipped with 15.8GB of memory. In my case, I used Google Cloud Platform.
* Machine Type: n1-standard-4
* GPU: 1 x NVIDIA Tesla T4 
* Cores: 2
* Memory: 15.8GB
* Operating System: Deep Learning on Linux
* OS version: Deep Learning VM with CUDA 11.8 M116 : Debian 11, Python 3.10. With CUDA 11.8 preinstalled.
# Git File Upload Server
* Set up a git file upload server on the created Virtual Machine instance.
```console
# Example command for setting up git file upload server
git init --bare my-repo.git
```
# Installing Requirements
* In the server console, run the following command to install the necessary requirements:
```console
pip install -r requirements.txt
```
* In my case, I installed only "my_install_package.txt"
# Running the Server
* Execute the following command to run the server:
```console
uvicorn server:app --reload --host=x.x.x.x --port=x
```
* If you encounter an FFmpeg error, resolve it by running the following command in the server console:
```console
conda install ffmpeg
```
* Make sure to replace x.x.x.x with the desired host IP address and x with the preferred port number.
