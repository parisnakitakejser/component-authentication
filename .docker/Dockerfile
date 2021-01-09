FROM python:3.8-alpine

EXPOSE 5000/tcp

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

RUN rm -rf .env

CMD [ "python", "./app.py" ]