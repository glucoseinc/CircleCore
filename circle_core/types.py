import decimal
import os
import uuid
from typing import Any, Dict, NewType, Union

Path = Union[str, os.PathLike]
JSON = Dict[str, Any]
Payload = Dict[str, Any]
Timestamp = decimal.Decimal
Topic = NewType('Topic', str)


class BlobMetadata:
    # データを持っているホストのCcInfo.uuid, Noneは自分
    source: uuid.UUID
    # 中身のcontent type
    content_type: str
    # Blobのハッシュ値
    datahash: str

    def __init__(self, source: uuid.UUID, content_type: str, datahash: str):
        self.source = source
        self.content_type = content_type
        self.datahash = datahash


__all__ = ('BlobMetadata', 'Path', 'Payload', 'Timestamp')
