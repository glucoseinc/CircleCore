import json
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .message import ModuleMessage
    from .types import BlobMetadata


def serialize(obj: Any) -> str:
    return json.dumps(obj, cls=CircleCoreEncoder, sort_keys=True)


# JSON Encoder/Decoder
class CircleCoreEncoder(json.JSONEncoder):
    # override
    def default(self, o: Any) -> Any:
        from .message import ModuleMessage
        from .types import BlobMetadata

        if isinstance(o, ModuleMessage):
            return self.serialize_modulemessage(o)
        elif isinstance(o, BlobMetadata):
            return self.seriaze_blobmetadata(o)

        return super().default(o)

    def serialize_modulemessage(self, o: 'ModuleMessage') -> Any:
        return {'timestamp': str(o.timestamp), 'counter': o.counter, 'payload': o.payload, 'boxId': o.box_id.hex}

    def seriaze_blobmetadata(self, o: 'BlobMetadata') -> Any:
        return {
            '$type': o.content_type,
            '$data': o.datahash,
            '$source': str(o.source),
        }
