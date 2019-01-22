# -*- coding: utf-8 -*-
"""センサデータを受け取って保存するCircleModule"""

# system module
import asyncio
import base64
import logging
import os
import re
from hashlib import sha512
from typing import TYPE_CHECKING, cast
from uuid import UUID

# project module
from .base import CircleWorker, WorkerType, register_worker_factory
from ..types import BlobMetadata

if TYPE_CHECKING:
    from tuping import Optional

    from ..models import MessageBox

logger = logging.getLogger(__name__)
WORKER_BLOBSTORE = cast(WorkerType, 'blobstore')

DATA_URL_RE = re.compile(r'^data:(?P<content_type>\w+/\w+)(?:;(?P<base64>\w+)),')


# Blob
class StoredBlob(BlobMetadata):
    # content_type: str
    # datahash: str
    saving: 'Optional[asyncio.Future]'

    # public
    def __init__(self, source: UUID, content_type: str, datahash: str):
        super().__init__(source, content_type, datahash)
        self.saving = None

    @classmethod
    def save(cls, repos_dir: str, mbox: 'MessageBox', content_type: str, data: bytes) -> 'StoredBlob':
        # calc hash
        datahash = sha512(data).hexdigest()

        saving = asyncio.ensure_future(cls._save_async(cls.make_path(repos_dir, mbox, datahash), data))
        cc_info = mbox.module.cc_info
        stored_blob = cls(cc_info.uuid, content_type, datahash)
        stored_blob.saving = saving
        return stored_blob

    # private
    @classmethod
    def make_path(self, repos_dir: str, mbox: 'MessageBox', datahash: str) -> str:
        cc_info = mbox.module.cc_info
        return os.path.join(repos_dir, str(cc_info.uuid), str(mbox.uuid), datahash[:2], datahash[2:4], datahash)

    @classmethod
    async def _save_async(cls, path, data):
        dirpath = os.path.split(path)[0]
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        with open(path, 'wb') as fp:
            fp.write(data)


# BlobStoreWorker
@register_worker_factory(WORKER_BLOBSTORE)
def create_blobstore_worker(core, type, key, config):
    assert type == WORKER_BLOBSTORE
    # defaults = {'blob_dir': '${prefix}/blob'}
    defaults = {}
    return BlobStoreWorker(
        core,
        key,
        # db_url=config.get('db'),
        # time_db_dir=config.get('time_db_dir'),
        repos_dir=config.get('blob_dir', vars=defaults),
        # cycle_time=config.getfloat('cycle_time', vars=defaults),
        # cycle_count=config.getint('cycle_count', vars=defaults),
    )


class BlobStoreWorker(CircleWorker):
    """
    request_socketに届いた、生のメッセージのスキーマをチェックしたあと、プライマリキーを付与してDBに保存する。
    また、同時にhubにも流す。
    """
    worker_type = WORKER_BLOBSTORE

    def __init__(self, core, key, repos_dir):
        super(BlobStoreWorker, self).__init__(core, key)
        self.repos_dir = repos_dir

    def initialize(self):
        """override"""
        pass

    def finalize(self):
        """override"""
        pass

    # public
    def store_blob_url(self, mbox: 'MessageBox', data_url: str) -> StoredBlob:
        mo = DATA_URL_RE.match(data_url)
        if not mo:
            raise ValueError('invalid data url')

        content_type = mo.group('content_type')
        data = base64.b64decode(data_url[mo.end():])
        return self.store_blob(mbox, content_type, data)

    def store_blob(self, mbox: 'MessageBox', content_type: str, data: bytes) -> StoredBlob:
        stored_blob = StoredBlob.save(self.repos_dir, mbox, content_type, data)
        return stored_blob
