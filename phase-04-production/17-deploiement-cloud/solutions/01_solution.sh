# Module 17 — Solution exercice à trou #1

gunicorn \
    src.main:app \
    -w 9 \
    -k uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000
