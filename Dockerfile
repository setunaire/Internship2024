FROM python:3.11.10-slim-bookworm

WORKDIR /app

COPY requirement.txt ./

RUN pip install -r requirement.txt

COPY . .

EXPOSE 5005

CMD [ "flask", "run", "--host=0.0.0.0", "--port=5005"]