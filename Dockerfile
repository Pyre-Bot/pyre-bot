FROM python:3.8.5-slim-buster

WORKDIR /usr/src/app

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
 build-essential \
 gcc \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN BLIS_ARCH="generic" pip install spacy --no-binary blis \
 && pip install cython \
 && pip install --no-cache-dir -r requirements.txt \
 && python -m spacy download en

COPY cogs cogs/
COPY config/config.py config/
COPY libs libs/
COPY bot.py ./

CMD [ "python", "./bot.py" ]