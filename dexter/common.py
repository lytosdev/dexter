__tables_info = []


def __exist_tablename(dbo, name):
    for item in __tables_info:
        if item["schema"] + item["name"] == dbo + name:
            return __tables_info.index(item)
    return -1


def create_dbinfo(cursor):

    for row in cursor:
        result = __exist_tablename(row.TableSchema, row.TableName)
        if result == -1:
            __tables_info.append({
                "schema": row.TableSchema,
                "name": row.TableName,
                "fields": [{
                    "name": row.ColumnName,
                    "dataType": row.DataType,
                    "isIdentity": row.IsIdentity,
                    "isPrimaryKey": row.IsPrimaryKey,
                    "positionPrimaryKey": row.PositionPrimaryKey
                }]
            })
        else:
            table_info = __tables_info[result]
            table_info["fields"].append({
                "name": row.ColumnName,
                "dataType": row.DataType,
                "isIdentity": row.IsIdentity,
                "isPrimaryKey": row.IsPrimaryKey,
                "positionPrimaryKey": row.PositionPrimaryKey
            })

    return __tables_info


class CodeByLine:

    code = []

    def __init__(self):
        self.clear()

    def add(self, line, ntab=0):
        self.code.append("    " * ntab + line)

    def clear(self):
        self.code.clear()

    def get_code(self):
        return "\n".join(self.code)
