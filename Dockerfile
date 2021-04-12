FROM python:3.9

COPY requirements.txt requirements.txt
COPY files.py files.py
COPY main.py main.py

RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]