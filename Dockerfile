FROM python:3.8.5-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN python3 -m nltk.downloader punkt

COPY ./ ./

EXPOSE 5000

ENTRYPOINT bash -c "export PYTHONPATH=$PYTHONPATH:serverside && python3 scripts/create_db.py && python3 serverside/guampa.py"
