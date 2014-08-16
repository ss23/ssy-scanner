import boto.sqs, time, sys
from boto.sqs.message import Message
from boto.dynamodb2.table import Table

from libnmap.process import NmapProcess
from libnmap.parser import NmapParser, NmapParserException

from .BaseScanner import BaseScanner

class UpScanner(BaseScanner):
    def consume(self, targets):
        print(targets)
        nm = NmapProcess(targets, options='-v -sn')
        rc = nm.run()

        try:
            parsed = NmapParser.parse(nm.stdout)
        except NmapParserException as e:
            print("Exception raised while parsing scan: %s" % (e.msg))

        HOST_UP = 1
        HOST_DOWN = 0

        scans = Table('host_up', connection=self.dynamo)

        with scans.batch_write() as batch:
            for host in parsed.hosts:
                # Insert into database and delete from queue
                if (host.status == 'down'):
                    status = 0
                elif (host.status == 'up'):
                    status = 1
                else:
                    status = -1

                batch.put_item(data={
                    'ip': host.address,
                    'status': status,
                    'datetime': int(time.time())
                })
