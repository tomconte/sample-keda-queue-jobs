import os
import sys
import time
from azure.storage.queue import QueueClient

try:
  connection_string = os.environ['AzureWebJobsStorage']
  queue_name = os.environ['QUEUE_NAME']
except KeyError:
  print('Error: missing environment variable AzureWebJobsStorage or QUEUE_NAME')
  exit(1)

queue = QueueClient.from_connection_string(conn_str=connection_string, queue_name=queue_name)

for message in range(1, int(sys.argv[1])):
  queue.send_message(content='foo_'+str(message))
