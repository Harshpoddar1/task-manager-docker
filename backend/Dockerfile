# ---- Stage 1: Builder ----
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# ---- Stage 2: Final ----
FROM python:3.11-slim

WORKDIR /app

# Builder stage se sirf installed packages copy karo
COPY --from=builder /root/.local /root/.local

# App code copy karo
COPY . .

# PATH mein user-installed packages add karo
ENV PATH=/root/.local/bin:$PATH

EXPOSE 5000

CMD ["python", "app.py"]
