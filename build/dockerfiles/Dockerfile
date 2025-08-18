FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV TIMEZONE="Asia/Ho_Chi_Minh"

# Set dependencies path
ENV PYTHONPATH="/app"
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app/

COPY . /app/

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev iputils-ping telnet \
    && rm -rf /var/lib/apt/lists/*

RUN pip install uv 
RUN uv sync
