from uuid import uuid4
from pathlib import Path

import pytest

from circle_core.core.app import CircleCore
from circle_core.exceptions import MessageBoxNotFoundError
from circle_core.workers.datareceiver import WORKER_DATARECEIVER
import tests


def get_datareceiver():
    core = CircleCore.load_from_config_file(str(Path(tests.__path__[0]).joinpath('circle_core.ini')))
    return core.find_worker(WORKER_DATARECEIVER)


def test_invalid_message_box():
    resp = get_datareceiver().on_new_message({
        'box_id': uuid4().hex,
        'payload': {
            'hoge': 'piyo'
        }
    })
    assert resp['response'] == 'failed'
