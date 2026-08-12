# ── Stage: runtime ────────────────────────────────────────────
FROM python:3.12-slim

LABEL maintainer="cyber-course"
LABEL description="IDPS Simulation Web App for students"

WORKDIR /app

# Install dependencies first (cached unless requirements change)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app.py .

# Non-root user for security
RUN adduser --disabled-password --gecos "" appuser
USER appuser

EXPOSE 8080

# Use gunicorn for production (not Flask dev server)
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", \
     "--timeout", "30", "--access-logfile", "-", "app:app"]
