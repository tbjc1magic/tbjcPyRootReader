#include <Python.h>
#include <iostream>
#include <vector>
#include "TBJCCLASS.h"
#include "TTree.h"
#include "TFile.h"
#include "TROOT.h"
#include "TSystem.h"

using namespace std;

class FileReader 
{
   public:
       static FileReader* getInstance( )
		{
		    if(instance==0)
            {
                instance = new FileReader();
            }    
            
            return instance;
		}
    

       FileReader();

       int getV(){return value;}
       void setV(int v){value=v; }

        ~FileReader(){
            if(tbjcf) delete tbjcf;
            tbjctree = 0;
        }

        int getEntries(){return tbjctree->GetEntries();}
        PyObject* read(int idx);
        int open(const char*fname);
        
   private:

       PyObject* build_list(Int_t*p, int s);
       TFile* tbjcf;
       TTree* tbjctree;
       int value;
       static FileReader* instance;
       TBJCCLASS * carrier;
};



int FileReader:: open(const char* fname)
{
    if(tbjcf)tbjcf->Close();

    tbjcf = new TFile(fname);
    tbjctree = (TTree*)tbjcf->Get("tbjctree");

    tbjctree->SetBranchAddress("tbjcclass_branch",&carrier);
    return 1;
}



PyObject* FileReader:: read(int idx)
{

    tbjctree->GetEntry(idx);

    map<const char*, Int_t*> container; 

    container.insert(pair<const char*,Int_t*>("TDCData1",carrier->TDCData1));
    container.insert(pair<const char*,Int_t*>("AuxData1",carrier->AuxData1));
    container.insert(pair<const char*,Int_t*>("AuxData2",carrier->AuxData2));
    container.insert(pair<const char*,Int_t*>("PosData1",carrier->PosData[0]));
    container.insert(pair<const char*,Int_t*>("PosData2",carrier->PosData[1]));
    container.insert(pair<const char*,Int_t*>("PosData3",carrier->PosData[2]));
    container.insert(pair<const char*,Int_t*>("PosData4",carrier->PosData[3]));
    container.insert(pair<const char*,Int_t*>("ADCData1",carrier->ADCData[0]));
    container.insert(pair<const char*,Int_t*>("ADCData2",carrier->ADCData[1]));
    container.insert(pair<const char*,Int_t*>("ADCData3",carrier->ADCData[2]));
    container.insert(pair<const char*,Int_t*>("ADCData4",carrier->ADCData[3]));
    container.insert(pair<const char*,Int_t*>("ADCData5",carrier->ADCData[4]));
    
    map<const char*, Int_t*> :: iterator it; 

    PyObject* python_dict = PyDict_New();
    for(it=container.begin(); it!=container.end();it++)
    {
        PyObject* list = build_list(it->second, 16);
        PyObject* key = Py_BuildValue("s",it->first);
        PyDict_SetItem(python_dict, key, list);
        Py_DECREF(key);
        Py_DECREF(list);
    }
   
    //Py_DECREF(python_dict);

    return python_dict;
}




FileReader* FileReader:: instance=0;

FileReader::FileReader():tbjcf(0), tbjctree(0), carrier(0)
{
    gROOT->ProcessLine(".L TBJCCLASS.h+");
    carrier = new TBJCCLASS(); 
}


PyObject* FileReader::build_list(Int_t*p, int s)
{
    PyObject* python_list = PyList_New(s);
    for (int i=0; i<s; ++i)
    {
        PyObject* python_ele = Py_BuildValue("i", p[i]);
        PyList_SetItem(python_list, i, python_ele);
    }   
    
    return python_list;
}

static PyObject * read(PyObject *self, PyObject *args)
{
    int idx;

    if (!PyArg_ParseTuple(args, "i", &idx))
        return NULL;

    FileReader* fr = FileReader::getInstance();
    
    return fr->read(idx);

}

static PyObject * open(PyObject *self, PyObject *args)
{
    const char *file;

    if (!PyArg_ParseTuple(args, "s",  &file))
        return NULL;
    
    FileReader* fr = FileReader::getInstance();
    fr->open(file);
    
    return Py_None; 
}

static PyObject * getEntries(PyObject *self, PyObject *args)
{
    
    FileReader* fr = FileReader::getInstance();
    
    return Py_BuildValue("i", fr->getEntries()); 
}

static PyMethodDef tbjcPyRootReaderMethods[] = {
    {"getEntry",    read,       METH_VARARGS, "read a entry."},
    {"open",        open,       METH_VARARGS, "open a file."},
    {"getEntries",  getEntries, METH_VARARGS, "get # of counts."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef tbjcPyRootReaderModule = {
    PyModuleDef_HEAD_INIT,
    "tbjcPyRootReader",   /* name of module */
    NULL, /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    tbjcPyRootReaderMethods
};

PyMODINIT_FUNC
PyInit_tbjcPyRootReader(void)
{
    return PyModule_Create(&tbjcPyRootReaderModule);
}


int
main(int argc, char *argv[])
{
    wchar_t *program = Py_DecodeLocale(argv[0], NULL);
    if (program == NULL) {
        fprintf(stderr, "Fatal error: cannot decode argv[0]\n");
        exit(1);
    }

    /* Add a built-in module, before Py_Initialize */
    PyImport_AppendInittab("tbjcPyRootReader", PyInit_tbjcPyRootReader);

    /* Pass argv[0] to the Python interpreter */
    Py_SetProgramName(program);

    /* Initialize the Python interpreter.  Required. */
    Py_Initialize();

    /* Optionally import the module; alternatively,
       import can be deferred until the embedded script
       imports it. */
    PyImport_ImportModule("tbjcPyRootReader");


    PyMem_RawFree(program);
    return 0;
}
