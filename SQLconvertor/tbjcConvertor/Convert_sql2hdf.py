import pandas as pd
import numpy as np
from sqlalchemy import create_engine


def GetAuxData(con):
    TDCData1 = pd.io.sql.read_sql("SELECT ch0, ch1 FROM TDCData1", con=con)
    TDCData1.columns = ['Array RF', 'IC RF']

    AuxData1 = pd.io.sql.read_sql("SELECT ch0, ch12, ch13, ch14, ch15 FROM AUXData1", con=con)
    AuxData1.columns = ['TAC','IC0','IC1','IC2','IC3']

    AuxData = pd.concat([TDCData1, AuxData1], axis=1)

    return AuxData

def GetSiData(con):
    MapDet=[[ 1, 0, 5, 4, 3, 2, 1, 0, 3, 2, 1, 0, 5, 4, 3, 2],
		   [11,10, 9, 8, 7, 6, 5, 4, 7, 6,11,10, 9, 8, 7, 6],
		   [15,14,13,12,11,10, 9, 8,17,16,15,14,13,12,17,16],
			   [20,21,22,23,18,19,20,21,12,13,14,15,16,17,18,19],
			   [-1,-1,-1,-1,-1,-1,-1,-1,22,23,18,19,20,21,22,23]]; 
    MapSig=[[1,1,0,0,0,0,0,0,2,2,2,2,1,1,1,1], ## 0->E, 1->XF, 2->XN
			   [0,0,0,0,0,0,2,2,2,2,1,1,1,1,1,1],
			   [0,0,0,0,2,2,2,2,1,1,1,1,1,1,0,0],
			   [0,0,0,0,1,1,1,1,2,2,2,2,2,2,0,0],
		   [-1,-1,-1,-1,-1,-1,-1,-1,1,1,2,2,2,2,2,2]];

    E_df, XF_df, XN_df = [], [], []

    for i in range(5):
        _ADCData = pd.io.sql.read_sql("SELECT * FROM ADCData{}".format(i+1), con=con)
        _ADCData = _ADCData.set_index('ID')
        _ADCData.columns = MapDet[i]
        _E_df = _ADCData.loc[:,[_==0 for _ in MapSig[i]]]
        _XF_df = _ADCData.loc[:,[_==1 for _ in MapSig[i]]]
        _XN_df = _ADCData.loc[:,[_==2 for _ in MapSig[i]]]

        E_df.append(_E_df)
        XF_df.append(_XF_df)
        XN_df.append(_XN_df)

    E_df = pd.concat(E_df, axis=1)[list(range(24))]
    XF_df = pd.concat(XF_df, axis=1)[list(range(24))]
    XN_df = pd.concat(XN_df, axis=1)[list(range(24))]

    return E_df, XF_df, XN_df

def process(fin, fout):
    con = create_engine('sqlite+pysqlite:///'+fin)
    AuxData = GetAuxData(con)
    E_df, XF_df, XN_df = GetSiData(con)

    with pd.HDFStore(fout) as s:
        s['AuxData'] = AuxData
        s['E']  = E_df 
        s['XF'] = XF_df 
        s['XN'] = XN_df 

from . import Convertor_lite  
def main():
    Convertor_lite.process('034.root','tmp.db')
    process('tmp.db', 'abc.hdf5')


if __name__ == '__main__':
    main()

