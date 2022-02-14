from dexter.common import CodeByLine


def get_template(namespace, connection_string):

    code = CodeByLine()

    code.add("using System.Data.SqlClient;")
    code.add("")
    code.add(f"namespace {namespace}")
    code.add("{")
    code.add(f"public class GenericRepository", 1)
    code.add("{", 1)
    code.add("")

    code.add(f"protected SqlConnection dbConnection()", 2)
    code.add("{", 2)
    code.add(f"return new SqlConnection(\"{connection_string}\");", 3)
    code.add("}", 2)

    code.add("")
    code.add("}", 1)
    code.add("}")

    return code.get_code()
