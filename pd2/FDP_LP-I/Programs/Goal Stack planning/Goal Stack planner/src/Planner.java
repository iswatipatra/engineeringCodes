import java.util.ArrayList;
import java.util.Scanner;
import java.util.Stack;

public class Planner 
{
    int blocks;                        // number of blocks.
    String goal_s;                     // Goal string.
    State initial,goal,curr;           // State object for initial, current and final state of block world.
    Stack s;                           // Stack 
    ArrayList<String> steps;           // to store action taken.
    
    Planner(int b,String init,String last)
    {
    	blocks = b;
    	initial = new State(blocks,init);
    	goal = new State(blocks,last);
    	curr = new State(blocks,init);
    	s = new Stack();
    	goal_s = last;
    	steps = new ArrayList<String>();
    }
    
    void stackPlan()
    {
    	int i;
    	String g;
    	
    	s.push(goal_s);                                       // Push initial goal on stack.
    	String subG[] = goal_s.split("['^']+");
		for(i=subG.length-1;i>=0;i--)
			s.push(subG[i]);                                  // Also push the subgoals on stack.
		
		while(!s.isEmpty())
		{
			System.out.println(s);                            // print status of stack.
			g = (String)s.pop();                              // pop the element
			if(g.contains("^"))                               // if its a conjugate goal.
			{
				if(curr.check(g)==0)                          // if true do nothing.
				{           
					s.push(g);
					subG = g.split("['^']+");                 // else again push it on stack. 
					for(i=subG.length-1;i>=0;i--)
						 s.push(subG[i]);
				}
			}
			else if(g.contains("on") && curr.check(g)==0)                                      // if its ON predicate and its not true.
			 {
				String ele[] = g.split("[() ]+");                                              // push action and preconditions. 
				s.push("(stack " + ele[2].charAt(0) + " " + ele[3].charAt(0)  +")");           // Action.
				
				s.push("(clear "+ ele[3].charAt(0) +")^(hold "+ ele[2].charAt(0) +")");        // preconditions.
				s.push("(hold "+ ele[2].charAt(0) +")");                                       
				s.push("(clear "+ ele[3].charAt(0) +")");
				
			 }
			else if(g.contains("ontable") && curr.check(g)==0)                                 // if its ONTABLE predicate and not true.
			 {
				String ele[] = g.split("[() ]+");
				s.push("(release " + ele[2].charAt(0) + ")");                                  // push action and preconditions.
				
				s.push("(hold "+ ele[2].charAt(0) +")");
			 }
			else if(g.contains("clear") && curr.check(g)==0)                                   // if its CLEAR predicate and not true.
			 {
				String ele[] = g.split("[() ]+");
				if(curr.hold[ele[2].charAt(0)%97]==1 )                                         // not clear bcz of holding it.
				{
					s.push("(release " + ele[2].charAt(0)  +")");                              // Action and preconditions
					
				    s.push("(hold " + ele[2].charAt(0) +")");
				}
				else                                                                          // so it has an block above it.
				{
					int t =curr.checktop(ele[2].charAt(0));                                   // check which block is above it
					if(t!=-1)                                                                 // then push action and preconditions.          
					{
						s.push("(unstack "+ Character.toString((char)(t+97))+" " + ele[2].charAt(0)  +")");
					 
						s.push("(on "+ Character.toString((char)(t+97))+" " + ele[2].charAt(0) +")^"+"(clear "+ Character.toString((char)(t+97)) +")^"+"(AE)");
						s.push("(AE)");
					    s.push("(clear "+ Character.toString((char)(t+97)) +")");
					    s.push("(on "+ Character.toString((char)(t+97))+" " + ele[2].charAt(0) +")");
					}    
				}
			 }	
			else if(g.contains("hold") && curr.check(g)==0)                               //if its HOLD predicate and not true.
			 {
				String ele[] = g.split("[() ]+");
				if(curr.ontable[ele[2].charAt(0)%97]==1)                                  // if block is ontable then do this. 
				{
				   s.push("(pick "+ ele[2].charAt(0)  +")");                              // actions and preconditions.
				
				   s.push("(ontable " + ele[2].charAt(0) +")^"+"(clear "+ ele[2].charAt(0) +")^"+"(AE)");
			       s.push("(AE)");
				   s.push("(ontable " + ele[2].charAt(0) +")");
				   s.push("(clear "+ ele[2].charAt(0) +")");
				}
				else                                                                                           // if block is on some other block.
				{
					int t =curr.checkbottom(ele[2].charAt(0));                                                 // check the block on which it is resting.
					if(t!=-1)
					{                                                                                          // actions and preconditions.
						s.push("(unstack " + ele[2].charAt(0)+ " "+Character.toString((char)(t+97))  +")");
					 
						s.push("(on " + ele[2].charAt(0)+ " "+Character.toString((char)(t+97))  +")^"+"(clear "+ ele[2].charAt(0)  +")^(AE)");
						s.push("(AE)");
					    s.push("(clear "+ ele[2].charAt(0)  +")");
					    s.push("(on "+  ele[2].charAt(0)+ " "+Character.toString((char)(t+97))  +")");
					}    
				}
			 }
			else if(g.contains("AE") && curr.check(g)==0)                                           // Arm empty predicate
			{
				for(i=0;i<curr.blocks;i++)                                                         // release the holding block.
				{
					if(curr.hold[i]==1)
					{
						s.push("(release " + Character.toString((char)(i+97))  +")");
						
					    s.push("(hold " + Character.toString((char)(i+97)) +")");
					}
				}
			}
			else if(g.contains("pick") || g.contains("unstack") || g.contains("release") || g.contains("stack"))    // if an action the make appropriate changes to the world.
			{
				curr.performAction(g);
				steps.add(g);
			}
		}
		
		printSteps();
    }
    
    public void printSteps()
    {
    	System.out.println(""+steps);		
    }
    
	public static void main(String args[]) {
		
		int b;
		String init,goal;
		Scanner in = new Scanner(System.in);
		System.out.print("Enter number of blocks :");
		b=in.nextInt();
		
		in.nextLine();
		System.out.print("Enter initial state : ");
		init = in.nextLine();
		
		System.out.print("Enter goal state : ");
		goal = in.nextLine();
		
		Planner p = new Planner(b, init, goal);
		p.stackPlan();
		
		in.close();
	}
}
