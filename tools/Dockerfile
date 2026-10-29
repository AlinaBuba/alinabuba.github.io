# Screenshots without local Chrome: docker build -t alina-shots -f tools/Dockerfile . && docker run --rm -v "$PWD":/site alina-shots
FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends chromium fonts-liberation && rm -rf /var/lib/apt/lists/*
ENV CHROME=chromium
WORKDIR /site
CMD ["python3", "tools/shots.py"]
