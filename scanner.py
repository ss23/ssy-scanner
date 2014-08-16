import boto.sqs, time, sys
from boto.sqs.message import Message
import boto.dynamodb2
from boto.dynamodb2.table import Table

from scanners.UpScanner import UpScanner

# Set up connections, etc
conn = boto.sqs.connect_to_region('ap-southeast-2')
q = conn.create_queue('scan-queue')

ddbcon = boto.dynamodb2.connect_to_region('ap-southeast-2')

scanner = UpScanner(ddbcon)

while True:
    # 10 should be editable eventually
    rs = q.get_messages(num_messages=10, wait_time_seconds=1)

    if rs:
        targets = []
        for message in rs:
            targets.append(message.get_body().split(' ')[1])
        scanner.consume(targets)
        # We should check whether the scan worked first, but oh well
        for message in rs:
            q.delete_message(message)
        print(".", end="")
    else:
        print("+", end="")
        time.sleep(10)
        # We should have a test for "we've been here too long!"
    sys.stdout.flush()


