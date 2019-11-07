FROM python

WORKDIR /app

RUN pip install azure-storage-queue

COPY queue_consumer.py /app

CMD ["python", "queue_consumer.py"]
