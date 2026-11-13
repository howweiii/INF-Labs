FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV DATA_DIR=/app

COPY main.py product.py supplier.py inventory.py order.py discount.py test.py inventory.json products.csv ./

CMD ["python", "main.py"]