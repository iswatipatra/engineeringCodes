package homesearch.code;

import javax.servlet.annotation.*;
import java.io.*;
import java.sql.*;
import java.util.*;
import javax.servlet.*;
import javax.servlet.http.*;
import com.google.gson.*;

import homesearch.database.*;

@SuppressWarnings("serial")
@WebServlet("/searchApartments")
@MultipartConfig
public class SearchApartment extends HttpServlet {

	static Database db = new Database();
	
	@Override
	public void doPost(HttpServletRequest request, HttpServletResponse response)
			throws IOException, ServletException {
		String rooms = request.getParameter("rooms").toString();
		double rent = Double.parseDouble(request.getParameter("rent"));
		String city = request.getParameter("city").toString();
		String locality = request.getParameter("locality").toString();
		
		Map<String, Object> map = null;
		List<Map<String, Object>> mapList = new ArrayList<>();
		ResultSet rs = null;
		
		try {
			String query = "select * from house_details where city = ?";
			db.setStmt(query);
			db.stmt.setString(1, city);
			rs = db.stmt.executeQuery();
			
			while(rs.next()) {
				if(rent == 0.0 || rs.getDouble("rent") <= rent ) {
					if(locality.equals("") || rs.getString("locality").equals(locality)) {
						if(rooms.equals("Any") || rs.getString("num_of_bhk").equals(rooms)) {
							map = new LinkedHashMap<>();
							map.put("rooms", rs.getString("num_of_bhk"));
							map.put("rent", rs.getDouble("rent"));
							map.put("city", rs.getString("city"));
							map.put("locality", rs.getString("locality"));
							map.put("state", rs.getString("state"));
							map.put("phone", rs.getString("phone"));
							mapList.add(map);
						}
					}
				}
			}
		}
		catch(Exception ex) {
			ex.printStackTrace();
			response.getOutputStream().print("error");
			return;
		}
		
		String jsonData = new Gson().toJson(mapList);
		response.setContentType("application/json");
	    response.setCharacterEncoding("UTF-8");
	    response.getWriter().write(jsonData);
	}
	
	@Override
	public void destroy() {
		db.close();
	}
}
