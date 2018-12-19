# -*- coding: utf-8 -*-
import sqlalchemy

from circle_core.models import CcInfo, MetaDataBase, MetaDataSession


def setup_db():

    def create_own_cc_info():
        if not CcInfo.query.filter_by(myself=True).all():
            own_cc_info = CcInfo(
                display_name='Test CircleCore', uuid='FFFFFFFF-FFFF-4FFF-FFFF-FFFFFFFFFFFF', myself=True, work='Test'
            )
            with MetaDataSession.begin():
                MetaDataSession.add(own_cc_info)

    engine = sqlalchemy.create_engine('sqlite:///:memory:')
    # engine = sqlalchemy.create_engine('sqlite:///test.sqlite3')
    MetaDataBase.metadata.create_all(engine)
    MetaDataSession.configure(bind=engine)
    create_own_cc_info()
