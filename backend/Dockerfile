FROM python:3.12-slim

WORKDIR /code

RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /code/app

ENV PYTHONPATH=/code

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]