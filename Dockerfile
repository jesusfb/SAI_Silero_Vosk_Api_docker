# Dockerfile to deploy a llama-cpp container with conda-ready environments

# docker pull continuumio/miniconda3:latest

ARG TAG=latest
FROM continuumio/miniconda3:$TAG

RUN apt-get update \
    && DEBIAN_FRONTEND="noninteractive" apt-get install -y --no-install-recommends \
        git \
        uvicorn \
        libportaudio2 \
        locales \
        sudo \
        build-essential \
        dpkg-dev \
        wget \
        openssh-server \
        ca-certificates \
        netbase\
        tzdata \
        nano \
        software-properties-common \
        python3-venv \
        python3-tk \
        pip \
        bash \
        ncdu \
        ffmpeg \
        net-tools \
        openssh-server \
        libglib2.0-0 \
        libsm6 \
        libgl1 \
        libxrender1 \
        libxext6 \
        ffmpeg \
        wget \
        curl \
        psmisc \
        rsync \
        vim \
        unzip \
        htop \
        pkg-config \
        libcairo2-dev \
        libgoogle-perftools4 libtcmalloc-minimal4  \
    && rm -rf /var/lib/apt/lists/*

# Setting up locales
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8

# Create user:
RUN groupadd --gid 1020 silero-group
RUN useradd -rm -d /home/silero-user -s /bin/bash -G users,sudo,silero-group -u 1000 silero-user

RUN python3 -m pip install torch torchvision torchaudio

# Устанавливаем модуль для озвучивания текста:
RUN python3 -m pip install silero

# Устанавливаем модуль для распознавания текста:
RUN python3 -m pip install vosk

# Воспроизведение из контейнера:
#RUN python3 -m pip install sounddevice

# Сервер Flask:
#RUN python3 -m pip install flask

# FastApi
RUN python3 -m pip install pydantic uvicorn[standard] fastapi

RUN python3 -m pip install torch torchvision torchaudio

# Update user password:
RUN echo 'silero-user:admin' | chpasswd

RUN mkdir /home/silero-user/silero

RUN mkdir /home/silero-user/silero/src

RUN mkdir /home/silero-user/silero/model

RUN cd /home/silero-user/silero

# Тут переместить app.py в корень (для fastapi, все переезжает в папку до src)
#ADD src/app.py /home/silero-user/silero/src
ADD src/fast.py /home/silero-user/silero/src
ADD src/tts.py /home/silero-user/silero/
ADD src/stt.py /home/silero-user/silero/

#COPY model/vosk/complete /home/silero-user/silero/src/model
COPY model/vosk/complete/small4/model /home/silero-user/silero/model

# ----------------------------- Сборка Rest-api:
# Clone the repository
#RUN git clone https://github.com/snakers4/silero-models.git /home/silero-user/silero/sm/ && \
#    cd /home/silero-user/silero/sm/ && \
#    python3 -m pip install -r /home/silero-user/silero/sm/requirements.txt

# установка api
#RUN pip3 install silero-api-server

#RUN mkdir /home/silero-user/silero/example
#ADD src/example /home/silero-user/silero/example

#RUN git clone https://github.com/snakers4/silero-models.git /home/silero-user/silero/api/ && \
#    git pull && \
#    chmod 777 /home/silero-user/silero/api && \
#    python3 -m pip install -r /home/silero-user/silero/api/requirements.txt

# (Optional) Set PORT environment variable
#RUN export PORT=5000

# Preparing for login
RUN chmod 777 /home/silero-user/silero
ENV HOME /home/silero-user/silero/
# ENV HOME /home/silero-user/silero/src
WORKDIR ${HOME}
USER silero-user
#CMD python3 app.py --host=0.0.0.0

CMD uvicorn src.fast:app --host 0.0.0.0 --port 8083 --reload

#CMD python -m silero_api_server
#CMD python3 -m flask run --host=0.0.0.0
#CMD python3 __main__.py

# Docker:
# docker build -t sai .
# docker run -it -dit --name sai -p 8083:8083  --gpus all --restart unless-stopped sai:latest

# Debug:
# docker container attach sai