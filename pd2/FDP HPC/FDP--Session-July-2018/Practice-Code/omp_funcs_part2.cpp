/*Reduction Operations   
An example of a reduction operation is a summation:

for(i=1; i<=n; i++)
	{
	   sum = sum + a[i];
	}

 
How reduction works:

    1. "sum" is the reduction variable
    2.  cannot be declared shared
    3.  threads would overwrite the value of sum cannot be declared private
    4. private variables don't persist outside of parallel region specified reduction operation performed on individual values from each thread

*/




#include<stdio.h>
#include<iostream>
#include<omp.h>
using namespace std;
int main()
{

int sum=0,i,n=5,a[]={1,1,1,1,1};

//OMP parallel FOR loop
#pragma omp parallel for 
	for(i=0; i<n; i++) 
	{
	      sum = sum + a[i];
	      printf("\nThreadID,sum=(%d,%d)",omp_get_thread_num(),sum);
		
   	}
printf("\n Parallel \"FOR\" loop, SUM=%d\n",sum);


/***********************************************************************/







/*
The problem in that example was the race condition involving the result variable. 
The simplest solution is to eliminate the race condition by declaring a critical section.
This is a good solution if the amount of serialization in the critical section is small.
*/

sum=0;
//OMP parallel FOR loop with critical block
#pragma omp parallel for 
	for(i=0; i<n; i++) 
	{
	      #pragma omp critical
              {
	      sum = sum + a[i];
	      printf("\nThreadID,sum=(%d,%d)",omp_get_thread_num(),sum);
		}		
   	}
printf("\n Parallel with critical section \"FOR\" loop, SUM=%d\n",sum);


/***********************************************************************/
sum=0;

//OMP parallel FOR loop with reduction variable
#pragma omp parallel for reduction(+:sum)
  	 for(i=0; i<n; i++) 
	{
      	      sum = sum + a[i];
	      printf("\nThreadID,sum=(%d,%d)",omp_get_thread_num(),sum);
   	}

printf("\n Parallel \"FOR\" loop (After reduction), SUM=%d\n",sum);

return 0;
}


/*

output



guest-f9QUQv@c05l0124-OptiPlex-9020:~$ g++ omp_funcs_part2.cpp -fopenmp
guest-f9QUQv@c05l0124-OptiPlex-9020:~$ ./a.out

ThreadID,sum=(0,1)
ThreadID,sum=(0,5)
ThreadID,sum=(2,2)
ThreadID,sum=(1,4)
ThreadID,sum=(3,3)
 Parallel "FOR" loop, SUM=5

ThreadID,sum=(0,1)
ThreadID,sum=(0,2)
ThreadID,sum=(1,3)
ThreadID,sum=(2,4)
ThreadID,sum=(3,5)
 Parallel with critical section "FOR" loop, SUM=5

ThreadID,sum=(1,1)
ThreadID,sum=(3,1)
ThreadID,sum=(2,1)
ThreadID,sum=(0,1)
ThreadID,sum=(0,2)
 Parallel "FOR" loop (After reduction), SUM=5













*/
