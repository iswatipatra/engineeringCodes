
public class State 
{
    int blocks;                // Number of blocks.
	int on[][];                // matrix to denote (on A B) like on[A][B]=1.
	int ontable[];             // for ontable predicate.
	int clear[];               // for clear predicate.
	int hold[];                // for hold predicate.
	int arm;                   // Arm empty flag.   arm=1 thus arm empty.
	
	State(int n,String desc)
	{
		blocks =n;
		on = new int[n][n];
		ontable = new int[n];
		clear = new int[n];
		hold = new int[n];
		arm =-1;
		setState(desc);
	}
	
	void setState(String desc)                            // make changes to data structure according to given statement.
	{
		int i;
		String subG[] = desc.split("['^']+");
		for(i=0;i<subG.length;i++)
		{
			String ele[] = subG[i].split("[() ]+");
			if(ele[1].equals("on"))
			{
				on[(int)ele[2].charAt(0)%97][(int)ele[3].charAt(0)%97] = 1;
			}
			else if(ele[1].equals("ontable"))
			{
				ontable[ele[2].charAt(0)%97] =1;
			}
			else if(ele[1].equals("clear"))
			{
				clear[ele[2].charAt(0)%97] =1;
			}
			else if(ele[1].equals("hold"))
			{
				hold[ele[2].charAt(0)%97] =1;
			}
			else if(ele[1].equals("AE"))
			{
				arm =1;
			}
			
		}
		
	}
    
	public int check(String state)                     // checks whether the given goal is satisfied or not.
	{
		int i;
		String subG[] = state.split("['^']+");
		int flag=1;
		for(i=0;i<subG.length;i++)
		{
			String ele[] = subG[i].split("[() ]+");
	
			if(ele[1].equals("on") && on[(int)ele[2].charAt(0)%97][(int)ele[3].charAt(0)%97] == 1)
			{
				flag=1;
			}
			else if(ele[1].equals("ontable") && ontable[ele[2].charAt(0)%97] ==1)
			{
				flag =1;
			}
			else if(ele[1].equals("clear") && clear[ele[2].charAt(0)%97] ==1)
			{
				flag= 1;
			}
			else if(ele[1].equals("hold") && hold[ele[2].charAt(0)%97] ==1)
			{
				flag= 1;
			}
			else if(ele[1].equals("AE") && arm==1)
			{
				flag= 1;
			}
			else                              // if even a single goal is not satisfied return 0.
			  return 0;
		}
		return flag;
	}
	
	public int checktop(char c)               // check which block rest above a given block.
	{
		int i=0;
		for(i=0;i<blocks;i++)
		{
			if(on[i][c%97]==1)
				return i; 
		}
		return -1;
	}
	
	public int checkbottom(char c)          // check which block is below a given block.
	{
		int i=0;
		for(i=0;i<blocks;i++)
		{
			if(on[c%97][i]==1)
				return i; 
		}
		return -1;
	}
	
	public void performAction(String act)                      // Make appropriate changes to data structure for an action.
	{
		String ele[] = act.split("[() ]+");
		if(act.contains("pick"))                               // (pick A)
		  {
			 ontable[ele[2].charAt(0)%97]=0;                   // not ontable A
			 clear[ele[2].charAt(0)%97]=0;                     // not clear A
			 hold[ele[2].charAt(0)%97]=1;                      // hold A true 
			 arm=0;                                            // arm not empty 
	  	  }
		else if(act.contains("unstack"))                       // (unstack A B)  
		{
			hold[ele[2].charAt(0)%97]=1;                       // hold A
			clear[ele[2].charAt(0)%97]=0;                      // not clear A
			clear[ele[3].charAt(0)%97]=1;                      // clear B
			on[ele[2].charAt(0)%97][ele[3].charAt(0)%97]=0;    // on[A][B]=0
			arm=0;                                             // arm not empty 
		}
		else if(act.contains("release"))                       // (release A)
		{
			ontable[ele[2].charAt(0)%97]=1;                    //  ontable A true
			clear[ele[2].charAt(0)%97]=1;                      //  clear A true
			hold[ele[2].charAt(0)%97]=0;                       //  hold A not true
			arm=1;                                             // arm empty.
		}
		else if(act.contains("stack"))                         // (stack A B)
		{ 
			hold[ele[2].charAt(0)%97]=0;                       // hold A not true.
			clear[ele[2].charAt(0)%97]=1;                      // clear A true
			clear[ele[3].charAt(0)%97]=0;                      // clear B not true
			on[ele[2].charAt(0)%97][ele[3].charAt(0)%97]=1;    // on[A][B] = true.
			arm=1;                                             // arm empty.
		}
	}
	
}
