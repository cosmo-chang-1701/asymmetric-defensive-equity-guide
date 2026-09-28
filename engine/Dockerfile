FROM python:3.12-slim

WORKDIR /app

COPY engine/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY engine/ /app/engine/
COPY tests/ /app/tests/
COPY examples/ /app/examples/

ENV PYTHONPATH=/app

CMD ["pytest", "-v", "tests/"]
