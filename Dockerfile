FROM python:3.9

COPY requirements.txt requirements.txt
COPY historic_data.json historic_data.json
COPY main.py main.py

RUN pip install -r requirements.txt

CMD ["python3", "main.py"]