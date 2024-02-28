FROM python:3.11
WORKDIR /code
COPY . /code
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install -r requirements.txt
CMD ["uvicorn", "fast:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]