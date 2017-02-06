# # -*- coding: utf-8 -*-
# """WebSocketはTornado, HTTPはFlaskで捌く."""
# from tornado.ioloop import IOLoop
# from tornado.web import Application, FallbackHandler
# from tornado.wsgi import WSGIContainer

# from .ws.module import ModuleHandler
# from .ws.replication_master import ReplicationMaster
# from .wui import create_app


# def run(port=5000, metadata=None, debug=True):
#     """TornadoサーバーとFlaskサーバーを立てる.

#     clickから起動される.
#     """
#     # meinheldとか使う場合はこのファイルに追記していくことになるのかな
#     print('start combined server')
#     flask_app = create_app(metadata)
#     tornado_app = Application([
#         (r'/replication/(?P<slave_uuid>[0-9A-Fa-f-]+)', ReplicationMaster),
#         (r'/module/(?P<module_uuid>[0-9A-Fa-f-]+)', ModuleHandler),
#         (r'.*', FallbackHandler, {'fallback': WSGIContainer(flask_app)})
#     ], debug=debug)  # tornado/autoreload.pyがエラーを吐くので本番では切る

#     tornado_app.listen(port)
#     IOLoop.current().start()
