FROM python:3.11-bookworm

ENV TZ=UTC \
    LANG=C.UTF-8 \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /app

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -qqr requirements.txt && pip install --no-cache-dir -qq gunicorn==21.2.0

COPY ./app.py ./app.py

VOLUME /app/Models

ENV PORT=8000

EXPOSE 8000

CMD ["gunicorn", "--workers=4", "app:app"]
