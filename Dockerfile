FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir pyTelegramBotAPI requests
CMD python3 main.py
