from dexter.csharp.sqlserver_dbtypes import types
from dexter.common import CodeByLine


def get_template(table, namespace):

    code = CodeByLine()
    table_name = table["name"]

    code.add(f"namespace {namespace}")
    code.add("{")
    code.add(f"public class {table_name}", 1)
    code.add("{", 1)
    for field in table['fields']:
        csharp_type = [item[1] for item in types if item[0] == field["dataType"]]
        columnType = "object" if len(csharp_type) == 0 else csharp_type[0]
        columnName = field["name"]
        code.add(f"public {columnType} {columnName} {{ get; set; }}", 2)
    code.add("}", 1)
    code.add("}")

    return code.get_code()
