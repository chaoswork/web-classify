// win_cDemo.cpp : 定义控制台应用程序的入口点。
//

#include "ICTCLAS30.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void KeyExtract(const char *sInput);
void FingerPrint(const char *sInput);

void FingerPrint(const char *sInput)
{
	//初始化分词组件
	if(!ICTCLAS_Init())
	{
		printf("ICTCLAS INIT FAILED!\n");
		return ;
	}


	//释放分词组件资源
	ICTCLAS_Exit();
}

void KeyExtract(const char *sInput)
{
	//初始化分词组件
	if(!ICTCLAS_Init())
	{
		printf("ICTCLAS INIT FAILED!\n");
		return ;
	}

    int nCount = ICTCLAS_GetParagraphProcessAWordCount(sInput);
	//分词。提取关键词
	result_t *result =(result_t*)malloc(sizeof(result_t)*nCount);
	ICTCLAS_ParagraphProcessAW(nCount,result);//获取结果存到客户的内存中

	//指纹提取，须在ICTCLAS_ParagraphProcessAW函数执行完后执行
	unsigned long lFinger = ICTCLAS_FingerPrint();

	char buf[100];
	memset(buf, 0, 100);
	sprintf(buf, "%x", lFinger);
	printf("%s\n", buf);

	//关键词提取，须在ICTCLAS_ParagraphProcessAW函数执行完后执行
	result_t *resultKey = (result_t*)malloc(sizeof(result_t)*nCount);
	int nCountKey;
	ICTCLAS_KeyWord(resultKey, nCountKey);

	for (int i=0; i<nCountKey; i++)
	{
		char buf[100];
		memset(buf, 0, 100);
		int index = resultKey[i].start;
        if( resultKey[i].weight>0)
        {
            memcpy(buf,(void *)(sInput+index), resultKey[i].length);
            printf("%s\t%d\n", buf, resultKey[i].weight);
        }
	}

	free(resultKey);
	free(result);
    
	//释放分词组件资源
	ICTCLAS_Exit();
}

int main(int argc,char* argv[])
{
    const char *sInput = argv[1];
	//指纹提取
	FingerPrint(sInput);

	//关键词提取
	KeyExtract(sInput);
	return 1;
}
