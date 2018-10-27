from . import Convert_sql2hdf 
from . import Convertor_lite  
def convert(fin, fout, ftmp='tmp.db'):
    Convertor_lite.process(fin, ftmp)
    Convert_sql2hdf.process(ftmp, fout)


