FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt .
RUN apt-get update \
 && apt-get install -y default-libmysqlclient-dev gcc \
 && pip install --upgrade pip \
 && pip install -r requirements.txt
COPY . /app/
RUN python app/manage.py collectstatic --noinput
CMD ["gunicorn", "issue_tracker.wsgi:application", "--config", "gunicorn.conf.py"]