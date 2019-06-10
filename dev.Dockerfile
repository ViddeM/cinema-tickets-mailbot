FROM python:3

RUN mkdir /usr/src/app

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV CINEMA_POSTGRES_USER cinema
ENV CINEMA_POSTGRES_PASSWORD password
ENV CINEMA_POSTGRES_HOST db
ENV CINEMA_POSTGRES_PORT 5432
ENV CINEMA_POSTGRES_DB cinema

EXPOSE 5000

CMD ["sh", "start.sh"]
