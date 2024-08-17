# docker file, Image, Container
FROM python:3.10

ADD main.py api_secrets.py us_states.json ./

RUN pip install requests polars

CMD ["python", "./main.py"]