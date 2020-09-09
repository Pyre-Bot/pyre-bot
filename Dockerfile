FROM python:slim

WORKDIR /usr/src/app

RUN apt-get update \
 && apt-get install -y --no-install-recommends gcc \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt \
 && python -m spacy download en

COPY cogs cogs/
COPY config/config.py config/
COPY libs libs/
COPY bot.py ./

CMD [ "python", "./bot.py" ]