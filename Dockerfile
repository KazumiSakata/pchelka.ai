FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
RUN useradd --uid 10001 --create-home app
COPY --chown=app:app public ./public
COPY --chown=app:app server.py .
USER 10001:10001
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=4s --start-period=10s --retries=3 CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/welcome.html', timeout=2).close()"]
CMD ["python", "server.py", "--host", "0.0.0.0"]
