FROM python:3.11

ENV RUN_ON_DOCKER Yes

RUN mkdir /todoapp
WORKDIR /todoapp

COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

COPY todoapp .

#WORKDIR src
#
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
