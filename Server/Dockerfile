FROM python:3-alpine3.18
WORKDIR /api
COPY . /api
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["python", "main.py"]