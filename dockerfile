FROM python:3.12.4-slim-bookworm

WORKDIR /usr/src/app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    pkg-config \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libfreetype6-dev \
    libportmidi-dev \
    python3-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    x11-xserver-utils \
    && rm -rf /var/lib/apt/lists/*

COPY ch1/old_roman_empire_quiz/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ch1/old_roman_empire_quiz/ .

ENV DISPLAY=host.docker.interna1:0

CMD ["python", "./main.py"]