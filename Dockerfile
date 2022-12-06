FROM python:3.10-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

ARG PROXY

RUN if [-z "$PROXY"]; then \
        pip install --no-cache-dir --upgrade -r /code/requirements.txt; \
    else \
        pip install --proxy "$PROXY" --no-cache-dir --upgrade -r /code/requirements.txt; \
    fi
   
COPY ./app /code/app

WORKDIR /code/app

CMD["uvicorn", "main:app", "--reload", "--proxy-headers", "--host","0.0.0.0", "-port", "80"]