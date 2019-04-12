FROM cbaxter1988/scoring_server:dev

COPY . /app

CMD  python /app/app.py -d