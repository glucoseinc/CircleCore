import uuid

import pytest

from circle_core.message import ModuleMessage
from circle_core.serialize import serialize
from circle_core.types import BlobMetadata
from circle_core.workers.blobstore import StoredBlob


@pytest.mark.parametrize(  # noqa: F811
    ('payload', 'expected'),
    [
        (
            {'data': BlobMetadata('text/plain', 'deadbeafdeadbeafdeadbeafdeadbeaf', None)},
            '''\
{"boxId": "539ce356a7cb4bfc853ec1a8147f021f", "counter": 0, "payload": {"data": {"$data": null, \
"$source": "text/plain", "$type": "deadbeafdeadbeafdeadbeafdeadbeaf"}}, "timestamp": "1545895047.000"}\
'''
        ),
        (
            {'data': StoredBlob('text/plain', 'deadbeafdeadbeafdeadbeafdeadbeaf', None)},
            '''\
{"boxId": "539ce356a7cb4bfc853ec1a8147f021f", "counter": 0, "payload": {"data": {"$data": null, \
"$source": "text/plain", "$type": "deadbeafdeadbeafdeadbeafdeadbeaf"}}, "timestamp": "1545895047.000"}\
'''
        )
    ]
)
def test_message_jsonize(payload, expected):
    message = ModuleMessage(uuid.UUID('539CE356-A7CB-4BFC-853E-C1A8147F021F'), '1545895047.000', 0, payload)
    serialized = serialize(message)
    assert serialized == expected
