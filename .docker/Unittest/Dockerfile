FROM python:3.8-alpine

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

RUN rm -rf .env

#docker build -t unittest . -f .docker\Unittest\Dockerfile

CMD [ "pytest", "unittest" ]
