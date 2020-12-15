package homesearch.code;

import javax.servlet.http.HttpServlet;
import homesearch.database.Database;
import java.io.IOException;
import java.sql.ResultSet;
import java.sql.SQLException;
import javax.servlet.ServletException;
import javax.servlet.annotation.MultipartConfig;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;

@SuppressWarnings("serial")
@WebServlet("/loginCheck")
@MultipartConfig
public class Login extends HttpServlet {
	private static Database db = new Database();
	
	@Override
	public void doPost(HttpServletRequest request, HttpServletResponse response)
			throws IOException, ServletException {
		
		try {
			String uname = request.getParameter("uname");
			String pass = request.getParameter("pass");
			
			String query = "select * from users where uname = ? and pass = ?;";
			db.setStmt(query);
			db.stmt.setString(1, uname);
			db.stmt.setString(2, pass);
			ResultSet rs = db.stmt.executeQuery();
			if(rs.next()) {				
				response.getWriter().print("success");
			}
			else {				
				response.getWriter().print("fail");
			}
		}
		catch(SQLException sqlex) {
			sqlex.printStackTrace();
		}
	}
}
