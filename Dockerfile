FROM python:3.11
LABEL authors="satish"

ADD requirements.txt .

RUN pip install --trusted-host pypi.python.org -r requirements.txt

CMD ["uvicorn", "api.main:app", "--reload","--host", "0.0.0.0", "--port", "80"]

