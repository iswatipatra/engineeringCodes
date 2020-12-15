package homesearch.code;

import java.io.IOException;
import java.sql.SQLException;
import javax.servlet.ServletException;
import javax.servlet.annotation.MultipartConfig;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import homesearch.database.Database;

@SuppressWarnings("serial")
@WebServlet("/register")
@MultipartConfig
public class Register extends HttpServlet {
	private static Database db = new Database();
	
	@Override
	public void doPost(HttpServletRequest request, HttpServletResponse response)
			throws IOException, ServletException {
		
		try {
			String uname = request.getParameter("uname");
			String pass = request.getParameter("pass");
			
			String query = "insert into users values(?, ?)";
			db.setStmt(query);
			db.stmt.setString(1, uname);
			db.stmt.setString(2, pass);
			db.stmt.executeUpdate();
			response.getWriter().write("success");
		}
		catch(SQLException sqlex) {
			sqlex.printStackTrace();
			response.sendError(1234);
		}
	}
}
