import uuid

class UuidUtil:

    @staticmethod
    def New() -> str:
        return str(uuid.uuid4())
