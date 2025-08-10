FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir openai aiogram flask redis
EXPOSE 8080

COPY handlers/controller.py /app/handlers/controller.py
COPY bot.py /app/bot.py
COPY sender.py /app/sender.py

CMD ["python", "./bot.py"]