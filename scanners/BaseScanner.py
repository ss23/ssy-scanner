class BaseScanner:
    def __init__(self, dynamo):
        self.dynamo = dynamo

    def consume(self, targets):
        raise NotImplementedError
