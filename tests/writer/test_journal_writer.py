# -*- coding: utf-8 -*-
import json
import os
from unittest.mock import MagicMock
import uuid

import pytest

from circle_core.message import ModuleMessage
from circle_core.models import MessageBox
from circle_core.writer.journal_writer import JournalWriter


def test_journal_open(tmpdir):
    # check dir is empty
    assert not os.listdir(tmpdir)

    # open writer
    child_writer_mock = MagicMock()
    writer = JournalWriter(child_writer_mock, tmpdir)

    files = os.listdir(tmpdir)
    assert 'journal.000' in files
    assert 'journal.pos' in files
    assert open(os.path.join(tmpdir, 'journal.000'), 'rt').read() == ''
    assert open(os.path.join(tmpdir, 'journal.pos'), 'rt').read() == '0\n0'

    # store message
    timestamp = 123456.789
    messagebox = MessageBox(uuid=uuid.uuid4())
    message = ModuleMessage(messagebox.uuid, timestamp, 0, {'x': 1, 'y': 2})
    writer.store(messagebox, message)
    del writer

    files = os.listdir(tmpdir)
    assert 'journal.000' in files
    assert 'journal.pos' in files

    ln = open(os.path.join(tmpdir, 'journal.000')).read()
    assert ln.endswith('\n')
    assert ln and json.loads(ln) == {
        'boxId': messagebox.uuid.hex,
        'timestamp': '123456.7890000000',
        'counter': 0,
        'payload': {
            'x': '1',
            'y': '2'
        }
    }
    assert open(os.path.join(tmpdir, 'journal.pos')).read() == '0\n0'

    # re-start journal
