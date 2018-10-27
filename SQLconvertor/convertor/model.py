from sqlalchemy import orm
import datetime
from sqlalchemy import schema, types



class Model(object):




    ###################################
    ############ rawadc ###############
    ###################################

    def __init__(self):
        self.metadata = schema.MetaData()

        self.cls_dict = {n:self.build_mapper(n) for n in ['TDCData1',
                       'AuxData1','AuxData2',
                       'PosData1','PosData2','PosData3','PosData4',
                       'ADCData1','ADCData2','ADCData3','ADCData4','ADCData5',
                       ]}
   
        #self.obj_dict = {}
        #for k,cls in self.cls_dict.items():
        #    obj = cls()
        #    for j in range(16):
        #        setattr(obj, 'ch'+str(j), None)
        #    self.obj_dict[k] = obj



    def build_mapper(self,name):

        NumOfCh = 16
        schemalist = [schema.Column('ch'+str(i), types.SMALLINT) for i in range(NumOfCh)]

        table = schema.Table(name, self.metadata,
            schema.Column('ID', types.Integer, primary_key=True, autoincrement=True ),
            *schemalist
        )

        cls = type(name,(),{})
        orm.mapper(cls, table)
        
        return cls


    def __getattr__(self,k):
        return self.obj_dict[k]


if __name__ == "__main__":
    model = Model()
    model.AuxData1
