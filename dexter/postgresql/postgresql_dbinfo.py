from dexter.common import create_dbinfo
import psycopg2

dbinfo_query = """
            SELECT t1.table_schema AS TableSchema,
                t1.table_name AS TableName,
                t1.column_name AS ColumnName,
                t1.data_type AS DataType,
                CASE WHEN t1.is_identity='NO' THEN 0 ELSE 1 END AS IsIdentity,
                CASE WHEN t3.constraint_name IS null THEN 0 ELSE 1 END AS IsPrimaryKey,
                t3.ordinal_position AS PositionPrimaryKey
            FROM information_schema.columns AS t1
            INNER JOIN information_schema.table_constraints AS t2
            ON t1.table_schema=t2.table_schema
                AND t1.table_name=t2.table_name
            LEFT JOIN information_schema.key_column_usage AS t3 
            ON t2.constraint_name=t3.constraint_name
                AND t2.constraint_schema=t3.constraint_schema
                AND t2.constraint_name=t3.constraint_name
                AND t1.column_name=t3.column_name
            WHERE t2.constraint_type='PRIMARY KEY'
            """


class PostgreSqlDbInfo:

    server = ""
    port = ""
    database = ""
    user = ""
    password = ""

    cnxn = None

    def __init__(self, server, port, database, user, password):
        self.server = server
        self.port = port
        self.database = database
        self.user = user
        self.password = password

    def __connection_test(self):
        try:
            self.cnxn = psycopg2.connect(
                host=self.server,
                port=self.port,
                dbname=self.database,
                user=self.user,
                password=self.password
            )
        except psycopg2.Error as ex:
            print(ex.args[1])
            return False
        return True

    def get_info(self):
        if self.__connection_test():
            cursor = self.cnxn.cursor()
            cursor.execute(dbinfo_query)
            return create_dbinfo(cursor)
        return False
