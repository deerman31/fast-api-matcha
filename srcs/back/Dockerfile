FROM python:3.11-slim-bullseye

WORKDIR /app

# Rust と必要なビルドツールをインストール
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    pkg-config \
    && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y \
    && . $HOME/.cargo/env

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./fast-api/ .
EXPOSE 8000

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]