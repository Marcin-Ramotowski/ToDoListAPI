FROM python:3.11.7-alpine
WORKDIR /app
COPY api .
RUN pip install -r requirements.txt
EXPOSE 80
CMD ["python3", "app.py"]
