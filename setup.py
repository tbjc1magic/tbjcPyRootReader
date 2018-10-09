from setuptools import setup, Extension

import os
cwd = os.getcwd()
print(cwd)
module1 = Extension('tbjcPyRootReader',
        sources = ['tbjcPyRootReader.cxx'],
        include_dirs=['/home/tbjc1magic/lsu_data/local/root/include',
                     cwd],
        library_dirs=['/home/tbjc1magic/lsu_data/local/root/lib',
                      cwd],
        extra_compile_args=['-std=c++11', '-m64', ],
        extra_link_args='-lGui -lCore -lImt -lRIO -lNet -lHist -lGraf -lGraf3d -lGpad -lTree -lTreePlayer -lRint -lPostscript -lMatrix -lPhysics -lMathCore -lThread -lMultiProc -pthread -lm -ldl -rdynamic'.split(),
        language='c++11'
        )                    

setup (name = 'PackageName',
        version = '1.0',
        description = 'This is a demo package',
        ext_modules = [module1],
        )
