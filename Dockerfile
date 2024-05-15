FROM ubuntu:latest
FROM python:3.12.0
LABEL authors="semcenkoaroslav"

WORKDIR /Task_program

COPY requirements.txt .

RUN pip install --no-cache-dir -r Task_program/requirements.txt -v

COPY . .

CMD ["python", "task.py"]

ENTRYPOINT ["top", "-b"]