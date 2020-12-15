package homesearch.database;

import java.sql.*;

public class Database {
	private final String JDBC_Driver = "com.mysql.cj.jdbc.Driver";
	private final String DB_URL = "jdbc:mysql://localhost/homesearch";
	
	private final String username = "root";
	private final String password = "root";
	
	public Connection conn = null;
	public PreparedStatement stmt = null;
	
	public Database()
	{		
		try
		{
			Class.forName(JDBC_Driver);
					
			conn = DriverManager.getConnection(DB_URL, username, password);
		}
		catch(SQLException sqlex)
		{
			sqlex.printStackTrace();
		}
		catch(Exception ex)
		{
			ex.printStackTrace();
		}
	}
	
	public void setStmt(String query) throws SQLException {
		stmt = conn.prepareStatement(query);
	}
	
	public void close()
	{		
		try
		{
			if(stmt != null) stmt.close();
			if(conn != null) conn.close();
		}
		catch(SQLException sqlex)
		{
			sqlex.printStackTrace();
		}
	}
}
