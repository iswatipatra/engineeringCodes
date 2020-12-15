/*
-----------------------------------------------------------------------------------------------
omp_get_thread_num() - Returns the thread number of the thread executing within its thread team.


Syntax

int omp_get_thread_num( );  
-----------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------
omp_get_num_threads() - Returns the number of threads in the parallel region.

Syntax:

int omp_get_num_threads( );  

-----------------------------------------------------------------------------------------------



"master-thread" is very similar to "single" with following differences:


   1.  "single" can be executed by whichever thread reaching the region first; 
   2.  "single" has an implicit barrier upon completion of the region, where all threads wait for synchronization, 
        while master doesn't have any.
   3.  "single" specifies that a section of code should be executed by single thread (not necessarily the master thread)


"single" and "critical" are two very different things. As you mentioned:

    "single" specifies that a section of code should be executed by "single" thread (not necessarily the master thread)
    "critical" specifies that code is executed by one thread at a time, 
     so the "single" will be executed only once while the "critical" will be executed as many times as there are of threads.


*/



#include<stdio.h>
#include<iostream>
#include<omp.h>
using namespace std;
int main()
{

int count,idval;

	//get the no. of threads before parallel block
	count=omp_get_num_threads();
	cout<<"\n Number of Threads:-  "<<count;


	//get the thread-id before parallel block
	idval=omp_get_thread_num();
	cout<<"\nMaster-Thread ID:-  "<<idval<<endl;
	
	//get the no. of threads inside parallel block
	#pragma omp parallel
	{
		idval=omp_get_thread_num();			
		printf("\n Hello:- I am Thread No. %d\n",idval);


                //The omp single directive identifies a section of code that must be run by a single available thread.
		#pragma omp single
		{
		count=omp_get_num_threads();
		cout<<"\n Number of Threads (Inside Parallel Block):-  "<<count<<endl;
		}



		//get the thread-id inside parallel block.....
		cout<<"\n Thread ID:-  "<<omp_get_thread_num()<<endl;
                //its..ohhhhh... output is nasty we will keep it exclusive
		
		
		//"critical" specifies that code is executed by one thread at a time
		#pragma omp critical
			{
		cout<<"\n Critical Section-Thread ID:-  "<<omp_get_thread_num()<<endl;
			}

	}



return 0;
}


/*


********observe below error***************act accordingly************************

guest-f9QUQv@c05l0124-OptiPlex-9020:~$ g++ omp_funcs_part1.cpp
/tmp/cc2cvM3h.o: In function `main':
omp_funcs_part1.cpp:(.text+0x9): undefined reference to `omp_get_num_threads'
omp_funcs_part1.cpp:(.text+0x2d): undefined reference to `omp_get_thread_num'
collect2: error: ld returned 1 exit status
guest-f9QUQv@c05l0124-OptiPlex-9020:~$ g++ omp_funcs_part1.cpp -fopenmp
guest-f9QUQv@c05l0124-OptiPlex-9020:~$ ./a.out


********act accordingly************ use "fopenmp" for parallel prog execution ************

guest-f9QUQv@c05l0124-OptiPlex-9020:~$ g++ omp_funcs_part1.cpp -fopenmp
guest-f9QUQv@c05l0124-OptiPlex-9020:~$ ./a.out

 Number of Threads:-  1
 Master-Thread ID:-  0

 Hello:- I am Thread No. 0

 Number of Threads (Inside Parallel Block):-  4

 Hello:- I am Thread No. 2

 Hello:- I am Thread No. 1

 Hello:- I am Thread No. 3

 Thread ID:-  3

 Critical Section-Thread ID:-  3

 Thread ID:-  2

 Thread ID:-  0

 Thread ID:-  1

 Critical Section-Thread ID:-  1

 Critical Section-Thread ID:-  2

 Critical Section-Thread ID:-  0










*/
