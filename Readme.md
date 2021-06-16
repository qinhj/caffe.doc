## Preparation ##
```
## caffe dependencies
$ sudo apt-get install libprotobuf-dev libleveldb-dev libsnappy-dev libopencv-dev libhdf5-serial-dev protobuf-compiler
$ sudo apt-get install --no-install-recommends libboost-all-dev
$ sudo apt-get install libopenblas-dev liblapack-dev libatlas-base-dev
$ sudo apt-get install libgflags-dev libgoogle-glog-dev liblmdb-dev
$ sudo apt-get install git cmake build-essential

## smoke check
$ protoc --version
libprotoc 3.0.0

## smoke test
$ vi test.cpp
#include <iostream>
#include <boost/array.hpp>
using namespace std;
int main(){
  boost::array<int, 4> arr = {{1,2,3,4}};
  cout << "hello world!" << arr[0]<<endl;
  return 0;
}
$ g++ -o demo test.cpp -lstdc++
$ ./demo
hello world!

## with opencv3.2.0
$ cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local ..
$ make -j`nproc` && sudo make install
## Note: With high version cuda(e.g. cuda9/10.2/...), one may need to update the source code, then re-cmake as:
$ cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D CUDA_GENERATION=Kepler ..

## with python
## Note: When install numpy, the libgfortran4 and libopenblas will also be installed!
$ conda create -n caffe python=3.6 numpy -y
$ conda activate caffe
$ pip install pillow matplotlib opencv-python==3.4.2.17 -i https://pypi.doubanio.com/simple/
$ pip install scikit-image protobuf
```

## Install (with python) ##
```
## clone source code
$ git clone https://github.com/BVLC/caffe
$ cd caffe

## config makefile
$ cp Makefile.config.example Makefile.config
$ vim Makefile.config # e.g. caffe/Makefile.config.cpu.miniconda3
* Note:
1) Before compile caffe, plz make sure caffe can find the right libgfortran.so for libopenblas.so.
For example, with ubuntu16.04, one may need to create softlink of libgfortran.so to /usr/local/lib
by update-alternative, and set /usr/local/lib before $(PYTHON_LIB) in LIBRARY_DIRS if use openblas,
since numpy will also install libgfortran4 and libopenblas to conda env lib.

## env var settings(necessary)
$ export CAFFE_ROOT=$HOME/desktop/caffe/
$ export PYTHONPATH=$CAFFE_ROOT/python:$PYTHONPATH
## or just source env.rc
$ source env.rc

## quick build
$ make -j`nproc`
$ make test -j`nproc`
$ make runtest -j`nproc` # optional
$ make py
```

## Prototxt ##
```
1. Add "engine: CAFFE" to your depthwise convolution layer to solve the memory issue.
```

## FAQ ##
```
0. fatal error: hdf5.h missing
$ pkg-config hdf5 --libs --cflags
-I/usr/include/hdf5/serial -L/usr/lib/x86_64-linux-gnu/hdf5/serial -lhdf5
line92: INCLUDE_DIRS := $(PYTHON_INCLUDE) /usr/local/include /usr/include/hdf5/serial/
line93: LIBRARY_DIRS := $(PYTHON_LIB) /usr/local/lib /usr/lib /usr/lib/x86_64-linux-gnu/hdf5/serial

1. compile caffe with python3.6
Note:
  caffe need protobuf < 3.0
  python3.6 only support protobuf >= 3.0
See https://blog.csdn.net/u011276025/article/details/100776461

2. math_functions.cpp:250] Check failed: a <= b (0 vs. -1.19209e-07)
Maybe it caused by the wrong label data, e.g. bbox out of image.
Solution: Comment line 250 in src/caffe/util/math_functions.cpp:
// CHECK_LE(a, b);
then "make py" again.

3. Data layer prefetch queue empty
https://github.com/BVLC/caffe/issues/3174
https://github.com/BVLC/caffe/issues/3177

4. nvcc fatal: Unsupported gpu architecture 'compute_20'
# CUDA architecture setting: going with all of them.
# For CUDA < 6.0, comment the *_50 through *_61 lines for compatibility.
# For CUDA < 8.0, comment the *_60 and *_61 lines for compatibility.
# For CUDA >= 9.0, comment the *_20 and *_21 lines for compatibility.

5. [OpenCV] CMake Error at cmake/OpenCVCompilerOptions.cmake:21 (else):
line21: -    else()
line22: -      message(STATUS "Looking for ccache - not found")

6. /usr/bin/ld: warning: libgfortran.so.4, needed by /home/qinhj/.conda/envs/caffe/lib/libopenblas.so, not found (try using -rpath or -rpath-link)
* Note: It seems that ubuntu16.04 only has libgfortran.so.3.
Solution: Check if you have the right libgfortran.so in library path.
## for ubuntu16.04 install gcc7 if necessary
$ sudo apt install gcc-7 g++-7 gfortran-7 # libgfortran4

7. /usr/bin/ld: cannot find -lboost_python3 (ubuntu16.04)
$ wget http://sourceforge.net/projects/boost/files/boost/1.67.0/boost_1_67_0.tar.gz
$ tar xvzf boost_1_67_0.tar.gz && cd boost_1_67_0/
$ ./bootstrap.sh --with-libraries=python --with-toolset=gcc
$ ./b2 --with-python include="/usr/include/python3.6m"
or one can simply try:
$ sudo ln -sf /usr/lib/x86_64-linux-gnu/libboost_python-py35.so /usr/lib/x86_64-linux-gnu/libboost_python3.so
```