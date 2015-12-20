# -*- coding: utf-8 -*-

try:
    import anydbm as dbm
    assert dbm
except ImportError:
    import dbm
import pickle
import logging
from redis import StrictRedis
from werobot.session import SessionStorage as SessionStorage
# from wechat.session.redisstorage import RedisStorage
from werobot.session.filestorage import FileStorage

logger = logging.getLogger(__name__)


class Session(SessionStorage):
    """extend for werobot SessionStorage"""
    def __init__(self):
        super(Session, self).__init__()

    def expire(self, key, expire_seconds):
        raise NotImplementedError()

    def exists(self, key):
        raise NotImplementedError()


class RedisSession(StrictRedis, Session):

    def get(self, name):
        pickled_value = super(RedisSession, self).get(name)
        if pickled_value is None:
            return None
        return pickle.loads(pickled_value)

    def set(self, name, value, ex=None, px=None, nx=False, xx=False):
        return super(RedisSession, self).set(
            name, pickle.dumps(value), ex, px, nx, xx
        )


class FileSession(Session):

    """
    FileSession 会把你的 Session 数据以 dbm 形式储存在文件中。

    :param filepath: 文件名， 默认为 ``coolcantonese_session``
    """
    def __init__(self, filepath='coolcantonese_session'):
        self.db = dbm.open(filepath, "c")

    def get(self, key):
        try:
            session_json = self.db[key]
        except KeyError:
            return None
        return pickle.loads(session_json)

    def set(self, key, value):
        self.db[key] = pickle.dumps(value)

    def delete(self, key):
        del self.db[key]

    def expire(self, key, expire_seconds):
        pass

    def exists(self, key):
        # logger.debug("db.keys:%s", self.db.keys())
        return key in self.db


class SmartSession(Session):
    """docstring for Session"""
    def __init__(self, cfg):
        super(SmartSession, self).__init__()
        if cfg.use_redis_session:
            self._session = RedisSession(
                cfg.redis_host, cfg.redis_port,
                cfg.redis_db, cfg.redis_password)
        else:
            self._session = FileSession(cfg.file_session_path)

    def get(self, key):
        return self._session.get(key)

    def set(self, key, value):
        return self._session.set(key, value)

    def delete(self, key):
        return self._session.delete(key)

    def expire(self, key, expire_seconds):
        return self._session.expire(key, expire_seconds)

    def exists(self, key):
        return self._session.exists(key)
