
# coding: utf-8


from sqlalchemy import *
from sqlalchemy import orm
import numpy as np

from model import Model
import tbjcPyRootReader
import time

def process(root_fname, sql_fname):
    engine = create_engine('sqlite+pysqlite:///{}'.format(sql_fname))

    model = Model()

    model.metadata.bind = engine
    model.metadata.create_all()

    # Set up the session
    sm = orm.sessionmaker(bind=engine, autoflush=True, autocommit=False,
        expire_on_commit=True)
    session = orm.scoped_session(sm)

    tbjcPyRootReader.open(root_fname)

    print(tbjcPyRootReader.getEntries())

    for i in range(tbjcPyRootReader.getEntries()):
        if i % 100 == 0: print(i)
        r = tbjcPyRootReader.getEntry(i)
        for k in r.keys():
            obj = model.cls_dict[k]()
            
            for j in range(16):
                setattr(obj, 'ch'+str(j), r[k][j])
            session.add(obj)

        if i %10000 == 0:
            session.commit()
    session.commit()
    import time

def main():

    start_time = time.time()
    process('034.root', 'abc.db')
    end_time = time.time()


    print(end_time - start_time)

if __name__ == "__main__":
    main()

