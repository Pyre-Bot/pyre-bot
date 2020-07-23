FROM python:slim

#RUN mkdir /data
#RUN mkdir /data/discord
#RUN mkdir /data/game_server_logs

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y gcc

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY cogs cogs/
COPY config config/
COPY libs libs/
COPY setup setup/
COPY bot.py ./

CMD [ "python", "./bot.py" ]