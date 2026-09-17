# ---- Stage 1: Builder ----
FROM python:3.11-slim AS builder
RUN apt-get update && apt-get upgrade -y

WORKDIR /app

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt && \
    pip install --upgrade pip setuptools wheel "jaraco.context>=6.1.0"

# ---- Stage 2: Final ----
FROM python:3.11-slim
RUN apt-get update && apt-get upgrade -y
WORKDIR /app

# Builder stage se sirf installed packages copy karo
COPY --from=builder /root/.local /root/.local

# App code copy karo
COPY . .

# PATH mein user-installed packages add karo
ENV PATH=/root/.local/bin:$PATH

EXPOSE 5000

CMD ["python", "app.py"]
