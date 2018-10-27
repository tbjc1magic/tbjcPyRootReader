from . import Convert_sql2hdf 
from . import Convertor_lite  
import os.path
def convert(fin, fout, ftmp='tmp.db'):
    if not os.path.isfile(fin):
        raise Exception("file does not exit")
    Convertor_lite.process(fin, ftmp)
    Convert_sql2hdf.process(ftmp, fout)


