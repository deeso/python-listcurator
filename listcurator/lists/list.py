from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *

import hashlib, os
from datetime import timedelta, datetime
from multiprocessing import Lock


class List(object):
    NAME = "List"
    @classmethod
    def get_name(cls):
        return cls.NAME

    def __init__(self, name, working_location=None, sqlitefile=None, days=30, hours=0):
        self.name = name
        self.days = days
        self.hours = hours
        self.in_memory_list = set()
        self.engine = None
        self.location = name+".db" if working_location is None else os.path.join(working_location, name+".db")
        if not sqlitefile is None:
            self.engine = create_engine('sqlite:///{0}'.format(sqlitefile))
        else:
            self.engine =  create_engine('sqlite:///{0}'.format(self.location))
        
        # self.metadata = MetaData(self.engine)
        self._Session = sessionmaker(bind=self.engine)
        self.ltable = None
        self.create_table()
        self._ListElement = self.generate_ListElement()
        self.load_keys()
        self.write_lock = Lock()
        # self.le_mapper = mapper(ListElement, self.ltable)

    def get_session(self):
        conn = self.engine.connect()
        return self._Session(bind=conn)

    def get_data(self, all_elements=False):
        session = self.get_session()
        cur = session.query(self._ListElement).all()
        res = []
        for i in cur:
            if not all_elements and not i.expired:
                res.append(i.key)
            elif all_elements:
                res.append(i.key)
        return "\n".join(sorted(res))

    def get_time_str(self, datetime_obj):
        return str(datetime_obj.strftime("%m-%d-%YT%H:%M"))

    def get_full(self, all_elements=False):
        session = self.get_session()
        cur = session.query(self._ListElement).all()
        res = []
        for i in cur:
            if not all_elements and not i.expired:
                res.append(" ".join([i.key, self.get_time_str(i.expires), i.comment]))
            elif all_elements:
                res.append(" ".join([i.key, self.get_time_str(i.expires), i.comment]))
        return "\n".join(sorted(res))


        return "\n".join(self.in_memory_list)

    def create_table(self):
        try:
            ltable = Table(self.name, MetaData(bind=self.engine),
                     Column('unique', String(64), primary_key=True),
                     Column('key', String()),
                     Column('expires', DateTime),
                     Column('expired', Boolean),
                     Column('comment', String()),)
            ltable.create()
        except:
            pass #raise
            # self.ltable = Table(self.name, MetaData(), autoload=True)

    def generate_ListElement(self):
        Base =  declarative_base()
        class ListElement(Base):
            __tablename__ = self.name
            unique = Column(String(64), primary_key=True)
            key = Column(String())
            expires = Column(DateTime)
            expired = Column(Boolean)
            comment = Column(String())

            NAME = "ListElement"
            @classmethod
            def get_name(cls):
                return cls.NAME


        return ListElement

    def updateexpiredkeys(self):
        session = self.get_session()
        now = datetime.now()
        cur = session.query(self._ListElement).all()
        self.in_memory_list = set()
        for instance in cur:
            if now > instance.expires:
                instance.expired = True
                # session.add(instance)

            if not instance.expired:
                self.in_memory_list.add(instance.key)
        session.commit()


    def load_keys(self):
        self.updateexpiredkeys()

    def get_element(self, key, session):
        return session.query(self._ListElement).filter_by(key=key).first()

    def get_elements(self, keys, session):
        r = [i for i in session.query(self._ListElement).filter(self._ListElement.key.in_(keys)).all()]
        return dict([(k.key,k) for k in r])

    def get_new_expire_time(self):
        return self.get_expires_time() + timedelta(days=self.days, hours=self.hours)

    def get_expires_time(self):
        dt = datetime.now()
        dt = datetime(dt.year, dt.month, dt.day, dt.hour)
        return dt

    def new_list_element(self, key, comment=''):
        unique = hashlib.md5(key).hexdigest()
        expires = self.get_new_expire_time()
        le = self._ListElement(expired=False, key=key, unique=unique, expires=expires, comment=comment)
        s = self.get_session()
        s.add(le)
        s.commit()
        return le

    def removekeys(self, keys, **kargs):
        session = self.get_session()
        les = self.get_elements(keys, session)
        res = dict([(k, None) for k in keys])

        for key in keys:
            if key in self.in_memory_list:
                self.in_memory_list.remove(key)
            le = les.get(key, None)
            if le is None:
                res[key] = False
            else:
                res[key] = True
                session.delete(le)
                
        session.commit()
        return res
     
    def addkeys(self, keys, **kargs):
        res = {}
        session = self.get_session()
        les = self.get_elements(keys, session)
        res = dict([(k, None) for k in keys])
        for key in keys:
            le = les.get(key, None)
            if not le is None and not le.expired:
                res[key] = False
            elif not le is None:
                res[key] = True
                le.expires = get_expires_time()
                le.expired = False
                session.add(le)
            elif le is None:
                res[key] = True
                le = self.new_list_element(key, comment='')
                
            self.in_memory_list.add(key)                

        session.commit()
        return res


    def addkeyscomments(self, keys_comments, **kargs):
        res = {}
        session = self.get_session()
        keys = [i[0] for i in keys_comments]
        les = self.get_elements(keys, session)
        res = dict([(k, None) for k in keys])
        for key, comment in keys_comments:
            le = les.get(key, None)
            if not le is None and not le.expired:
                res[key] = False
                le.comment = comment
            elif not le is None:
                res[key] = True
                le.expires = get_expires_time()
                le.expired = False
                le.comment = comment
                session.add(le)
            else:
                res[key] = True
                le = self.new_list_element(key, comment=comment)
            
            self.in_memory_list.add(key)                

        session.commit()
        return res

    def keysexist(self, keys):
        res = {}
        session = self.get_session()
        les = self.get_elements(keys, session)
        res = dict([(k, None) for k in keys])
        for key in keys:
            le = les.get(key, None)
            if le is None:
                res[key] = False
            else:
                res[key] = True
        return res

    def expirekeys(self, keys):
        res_keys = []
        self.updateexpiredkeys()
        session = self.get_session()
        les = self.get_elements(keys, session)
        res = dict([(k, None) for k in keys])
        for key in keys:
            le = les.get(key, None)
            if le is None:
                continue

            if key in self.in_memory_list:
                self.in_memory_list.remove(key)

            if not le.expired:
                res[key] = True
                le.expired = True
                le.expires = self.get_expires_time()
                # session.add(le)
            else:
                res[key] = False

        session.commit()
        return res
            
    def unexpirekeys(self, keys):
        res_keys = []
        self.updateexpiredkeys()
        session = self.get_session()
        les = self.get_elements(keys, session)
        res = dict([(k, None) for k in keys])
        for key in keys:
            le = les.get(key, None)
            if le is None:
                continue

            if key in self.in_memory_list:
                res[key] = False
                le.expires = self.get_new_expire_time()
                # session.add(le)
                continue
            elif not le is None:
                self.in_memory_list.add(le.key)
                res[key] = True
                le.expired = False
                le.expires = self.get_new_expire_time()
                # session.add(le)
        session.commit()
        return res
        
    def keysinfo(self, keys):
        session = self.get_session()
        les = self.get_elements(keys, session)
        res = dict([(k, None) for k in keys])
        for i in les:
            res[i.key] = {'expires':self.get_time_str(i.expires), 'expired':i.expired, 'comment':i.comment}
        return res

