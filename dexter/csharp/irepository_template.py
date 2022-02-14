from dexter.common import CodeByLine
from re import sub


def camelCase(string):
    string = sub(r"(_|-)+", " ", string).title().replace(" ", "")
    return string[0].lower() + string[1:]


def get_template(table, models_namespace, repositories_namespace):

    code = CodeByLine()
    table_name = table["name"]

    code.add(f"using {models_namespace};")
    code.add("using System.Collections.Generic;")
    code.add("using System.Threading.Tasks;")
    code.add("")

    code.add(f"namespace {repositories_namespace}")
    code.add("{")
    code.add(f"public interface I{table_name}Repository", 1)
    code.add("{", 1)

    code.add(f"Task<IEnumerable<{table_name}>> GetAll{table_name}();", 2)
    params = ["object " + camelCase(item["name"]) for item in table["fields"] if item["isPrimaryKey"] == 1]
    code.add(f"Task<{table_name}> Get{table_name}ById({', '.join(params)});", 2)
    code.add(f"Task<bool> Insert{table_name}({table_name} model);", 2)
    code.add(f"Task<bool> Update{table_name}({table_name} model);", 2)
    code.add(f"Task<bool> Delete{table_name}({table_name} model);", 2)

    code.add("}", 1)
    code.add("}")

    return code.get_code()
