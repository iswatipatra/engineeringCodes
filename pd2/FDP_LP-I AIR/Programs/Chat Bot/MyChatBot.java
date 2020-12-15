

package mychatbot;
import bitoflife.chatterbean.AliceBot;
import bitoflife.chatterbean.AliceBotMother;
import java.util.Scanner;

/**
 *
 * @author admin1
 */
public class MyChatBot {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
        Scanner sc=new Scanner(System.in);
        String ask;
        try{
            AliceBotMother mother=new AliceBotMother();
            AliceBot mybot=mother.newInstance();
            do{
            System.out.println("Enter Question: ");
            ask=sc.nextLine();
            String str=mybot.respond(ask);
            System.out.println(str);
            }while(!ask.equals("BYE"));
        }
        catch(Exception e)
        {
            System.err.println(e.toString());
        }
        
    }
    
}
