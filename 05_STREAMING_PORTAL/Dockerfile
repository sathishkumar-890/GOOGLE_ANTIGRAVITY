FROM python:3.11-slim

WORKDIR /app

# Copy proxy server script
COPY multi_stream_proxy.py .

# Expose default port
EXPOSE 8888

# Run with environment PORT support
CMD ["python", "multi_stream_proxy.py", "--host", "0.0.0.0"]
