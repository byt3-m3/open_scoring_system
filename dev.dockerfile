FROM cbaxter1988/scoring_server:base

COPY . /app

CMD  python /app/app.py -d