FROM python:3.8.13

WORKDIR /app

COPY . .

RUN apt update && apt install libopencv-dev -y && apt install cmake

RUN pip install -r requirements.txt


CMD ["python3","app.py"]
