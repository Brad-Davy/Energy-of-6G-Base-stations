FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip3 install numpy
RUN pip3 install matplotlib
RUN pip3 install flask
RUN pip3 install scipy

CMD ["python3", "/app/main.py"]

