FROM python:3.11.7-slim-bookworm
WORKDIR /app
COPY api .
RUN pip install -r requirements.txt
CMD python3 app.py
