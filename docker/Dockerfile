FROM python:3.7

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y poppler-utils ffmpeg libsm6 libxext6 libenchant-2-dev hunspell-de-de-frami tesseract-ocr tesseract-ocr-deu gcc

RUN mkdir /workdir

WORKDIR /workdir

COPY . .

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r main/src/requirements.txt

CMD ["/bin/bash", "/workdir/docker/runscript.sh"]
