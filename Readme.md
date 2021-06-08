## Preparation ##
```
## caffe dependencies
$ sudo apt-get install libprotobuf-dev libleveldb-dev libsnappy-dev libopencv-dev libhdf5-serial-dev protobuf-compiler
$ sudo apt-get install --no-install-recommends libboost-all-dev
$ sudo apt-get install libopenblas-dev liblapack-dev libatlas-base-dev
$ sudo apt-get install libgflags-dev libgoogle-glog-dev liblmdb-dev
$ sudo apt-get install git cmake build-essential
$ sudo apt-get install libboost-all-dev

## smoke checkout
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

## new conda environment
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

## quick build
$ make -j`nproc`
$ make py
$ make test -j`nproc`
$ make runtest -j`nproc` # optional
```

## FAQ ##
```
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
```