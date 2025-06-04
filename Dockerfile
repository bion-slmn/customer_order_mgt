FROM python:3.11-slim

# Create non-root user
RUN useradd -m -r appuser

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install psycopg2-binary


# Copy app files and set ownership
COPY --chown=appuser:appuser . .


# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Switch to non-root user
USER appuser

# Default command
CMD ["gunicorn", "customer_order.wsgi:application", "--bind", "0.0.0.0:8000"]

