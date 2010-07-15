/*
* svm.thrift
* xiaohui yan(l0he1g@gmail.com)
* 2010-06-19
*/

namespace cpp libsvm

service SVM{
	string predict( 1:string text ),
}
