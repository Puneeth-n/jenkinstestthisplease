FROM python:3.6

WORKDIR /opt/ct

EXPOSE 80

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD python app.py
