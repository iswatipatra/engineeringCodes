//set number of threads for parallelism
#include<stdio.h>
#include<iostream>
#include<cstdlib>
//****important to add following library to allow a programmer to use parallel paradigms*****
#include<omp.h>	
using namespace std;
#define MAX 50
int main()
{

//setting thread count outside parallel section

/********************

---->>>> if set_num_threads(x) doesnt work please disable dynamic team section for cutomizing number of thhreads like,


omp_set_dynamic(0);     // Explicitly disable dynamic teams
omp_set_num_threads(7); // Use 4 threads for all consecutive parallel regions


*********************/
omp_set_num_threads(MAX);

#pragma omp parallel
{
printf("\t Hello:%d\n",omp_get_thread_num());
}

cout<<"******************"<<endl;

//setting thread count with #pragma directive

#pragma omp parallel num_threads(15)
{
printf("\t World:%d\n",omp_get_thread_num());
}



}

/*
guest-ssxlhc@C04L0809:~$ ./a.out
	 Hello:4
	 Hello:28
	 Hello:23
	 Hello:24
	 Hello:9
	 Hello:11
	 Hello:12
	 Hello:26
	 Hello:27
	 Hello:0
	 Hello:29
	 Hello:30
	 Hello:31
	 Hello:32
	 Hello:33
	 Hello:5
	 Hello:34
	 Hello:35
	 Hello:6
	 Hello:36
	 Hello:7
	 Hello:37
	 Hello:8
	 Hello:38
	 Hello:10
	 Hello:39
	 Hello:13
	 Hello:40
	 Hello:41
	 Hello:14
	 Hello:42
	 Hello:15
	 Hello:43
	 Hello:16
	 Hello:44
	 Hello:17
	 Hello:45
	 Hello:18
	 Hello:46
	 Hello:19
	 Hello:47
	 Hello:48
	 Hello:20
	 Hello:21
	 Hello:22
	 Hello:2
	 Hello:1
	 Hello:49
	 Hello:3
	 Hello:25
******************
	 World:4
	 World:12
	 World:14
	 World:7
	 World:13
	 World:10
	 World:8
	 World:11
	 World:9
	 World:2
	 World:3
	 World:5
	 World:6
	 World:0
	 World:1
guest-ssxlhc@C04L0809:~$

*/
