package routines.system;

import java.sql.Connection;
import java.sql.SQLException;
import java.util.HashSet;
import java.util.Set;

public class TalendDataSource {

    private final javax.sql.DataSource ds;

    private Set<Connection> conns = new HashSet<>();

    /**
     * hold a data source inside
     * 
     * @param ds
     */
    public TalendDataSource(javax.sql.DataSource ds) {
        this.ds = ds;
    }

    /**
     * get the connection from the data source inside directly
     * 
     * @return
     * @throws SQLException
     */
    public java.sql.Connection getConnection() throws SQLException {
        Connection conn = ds.getConnection();
        if (conn != null) {
            conns.add(conn);
        }
        return conn;
    }

    /**
     * get the data source inside
     * 
     * @return
     */
    public javax.sql.DataSource getRawDataSource() {
        return ds;
    }

    /**
     * close all the connections which is created by the data source inside
     * 
     * @throws SQLException
     */
    public void close() throws SQLException {
        for (Connection conn : conns) {
            if (!conn.isClosed()) {// the connection can be closed outside
                conn.close();
            }
        }
        conns.clear();
    }
}
