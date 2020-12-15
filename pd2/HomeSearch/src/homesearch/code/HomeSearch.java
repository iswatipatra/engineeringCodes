package homesearch.code;

import homesearch.database.*;
import java.io.*;
import java.sql.SQLException;
import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.annotation.*;

@SuppressWarnings("serial")
@WebServlet("/submitDetails")
@MultipartConfig
public class HomeSearch extends HttpServlet {
	
	private static Database db = new Database();

	@Override
	public void doPost(HttpServletRequest request, HttpServletResponse response)
			throws IOException, ServletException {
		String rooms = request.getParameter("rooms").toString();
		double rent = Double.parseDouble(request.getParameter("rent").toString());
		String state = request.getParameter("state").toString();
		String city = request.getParameter("city").toString();
		String locality = request.getParameter("locality").toString();
		String phone = request.getParameter("phone").toString();
		
		try {
			String query = "insert into house_details values(default, ?, ?, ?, ?, ?, ?)";
			db.setStmt(query);
			db.stmt.setString(1, rooms);
			db.stmt.setDouble(2, rent);
			db.stmt.setString(3, state);
			db.stmt.setString(4, city);
			db.stmt.setString(5, locality);
			db.stmt.setString(6, phone);
			db.stmt.executeUpdate();
		}
		catch(SQLException sqlex) {
			sqlex.printStackTrace();
			response.getOutputStream().print("error");
			return;
		}
			   
		response.getOutputStream().print("done");
	}
	
	@Override
	public void destroy() {
		db.close();
	}
}