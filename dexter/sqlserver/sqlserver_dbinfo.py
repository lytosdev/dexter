from dexter.common import create_dbinfo
import pyodbc

dbinfo_query = """
            SELECT
                t1.TABLE_SCHEMA AS TableSchema,
            	t1.TABLE_NAME AS TableName,
            	t1.COLUMN_NAME AS ColumnName,
            	t1.DATA_TYPE AS DataType,
            	COLUMNPROPERTY(OBJECT_ID(t1.TABLE_NAME), t1.COLUMN_NAME, 'IsIdentity') AS IsIdentity,
            	IIF(t2.CONSTRAINT_TYPE='PRIMARY KEY', 1, 0) AS IsPrimaryKey,
            	ISNULL(t2.ORDINAL_POSITION, 0) AS PositionPrimaryKey
            FROM INFORMATION_SCHEMA.COLUMNS AS t1
            LEFT JOIN(
            	SELECT t1.TABLE_NAME, t1.COLUMN_NAME, t1.ORDINAL_POSITION, t2.CONSTRAINT_TYPE
            	FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS t1
            	LEFT JOIN INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS t2
                ON t1.CONSTRAINT_NAME=t2.CONSTRAINT_NAME
            	GROUP BY t1.TABLE_NAME, t1.COLUMN_NAME, t1.ORDINAL_POSITION, t2.CONSTRAINT_TYPE
                HAVING t2.CONSTRAINT_TYPE='PRIMARY KEY'
                ) AS t2
            ON t1.TABLE_NAME=t2.TABLE_NAME AND t1.COLUMN_NAME=t2.COLUMN_NAME
            """


class SqlServerDbInfo:

    driver = ""
    server = ""
    database = ""
    user = ""
    password = ""

    cnxn = None

    def __init__(self, driver, server, database, user, password):
        self.driver = driver
        self.server = server
        self.database = database
        self.user = user
        self.password = password

    def __connection_test(self):
        try:
            self.cnxn = pyodbc.connect(
                f"DRIVER={{{self.driver}}};SERVER={self.server};DATABASE={self.database};UID={self.user};PWD={self.password}")
        except pyodbc.Error as ex:
            print(ex.args[1])
            return False
        return True

    def get_info(self):
        if self.__connection_test():
            cursor = self.cnxn.cursor()
            cursor.execute(dbinfo_query)
            return create_dbinfo(cursor)
        return False
