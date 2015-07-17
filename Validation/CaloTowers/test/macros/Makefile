GCC=g++ -g `root-config --cflags --glibs` $< -o $@

all : singlePi.exe RelValMacro.so

singlePi.exe : SinglePi.C
	$(GCC)

RelValMacro.so : RelValMacro.C
	g++ -fPIC -shared RelValMacro.C -o RelValMacro.so -I /cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/boost/1.57.0-eccfad/include/ -I /cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/python/2.7.6-eccfad/include/python2.7 -L /cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/python/2.7.6-eccfad/lib -lpython2.7 -L /cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/boost/1.57.0-eccfad/lib -lboost_python -g `root-config --cflags --glibs`
