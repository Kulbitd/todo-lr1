FROM python:3.10-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

ARG PROXY

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

WORKDIR /code/app

CMD ["uvicorn", "main:app", "--reload", "--proxy-headers", "--host","0.0.0.0", "--port", "80"]