from dexter.common import CodeByLine
from dexter.csharp.sql_queries import get_query_selectall, get_query_selectbyid, get_query_insert, get_query_update, get_query_delete
import textwrap
from re import sub


def camelCase(string):
    string = sub(r"(_|-)+", " ", string).title().replace(" ", "")
    return string[0].lower() + string[1:]


def get_template(table, models_namespace, repositories_namespace):

    code = CodeByLine()
    table_name = table["name"]

    code.add("using Dapper;")
    code.add(f"using {models_namespace};")
    code.add("using System.Collections.Generic;")
    code.add("using System.Data.SqlClient;")
    code.add("using System.Threading.Tasks;")
    code.add("")

    code.add(f"namespace {repositories_namespace}")
    code.add("{")
    code.add(f"public class {table_name}Repository : GenericRepository, I{table_name}Repository", 1)
    code.add("{", 1)
    code.add("")

    code.add(f"public async Task<IEnumerable<{table_name}>> GetAll{table_name}()", 2)
    code.add("{", 2)
    code.add("var db = dbConnection();", 3)
    code.add("var sql =", 3)
    code.add(f"{textwrap.indent(get_query_selectall(table), '    ' * 4)};")
    code.add(f"return await db.QueryAsync<{table_name}>(sql);", 3)
    code.add("}", 2)
    code.add("")

    params = [f"object {camelCase(item['name'])}" for item in table["fields"] if item["isPrimaryKey"] == 1]
    obj = [item["name"] + " = " + camelCase(item["name"]) for item in table["fields"] if item["isPrimaryKey"] == 1]

    code.add(f"public async Task<{table_name}> Get{table_name}ById({', '.join(params)})", 2)
    code.add("{", 2)
    code.add("var db = dbConnection();", 3)
    code.add("var sql =", 3)
    code.add(f"{textwrap.indent(get_query_selectbyid(table), '    ' * 4)};")
    code.add(f"return await db.QueryFirstOrDefaultAsync<{table_name}>(sql, new {{ {', '.join(obj)} }});", 3)
    code.add("}", 2)
    code.add("")

    model = [f"{item['name']} = model.{item['name']}" for item in table["fields"] if item["dataType"] != "rowversion"]

    code.add(f"public async Task<bool> Insert{table_name}({table_name} model)", 2)
    code.add("{", 2)
    code.add("var db = dbConnection();", 3)
    code.add("var sql =", 3)
    code.add(f"{textwrap.indent(get_query_insert(table), '    ' * 4)};")
    code.add(f"var result = await db.ExecuteAsync(sql, new {{ {', '.join(model)} }});", 3)
    code.add("return result > 0;", 3)
    code.add("}", 2)
    code.add("")

    code.add(f"public async Task<bool> Update{table_name}({table_name} model)", 2)
    code.add("{", 2)
    code.add("var db = dbConnection();", 3)
    code.add("var sql =", 3)
    code.add(f"{textwrap.indent(get_query_update(table), '    ' * 4)};")
    code.add(f"var result = await db.ExecuteAsync(sql, new {{ {', '.join(model)} }});", 3)
    code.add("return result > 0;", 3)
    code.add("}", 2)
    code.add("")

    keys = [f"{item['name']} = model.{item['name']}" for item in table["fields"] if item["isPrimaryKey"] == 1]

    code.add(f"public async Task<bool> Delete{table_name}({table_name} model)", 2)
    code.add("{", 2)
    code.add("var db = dbConnection();", 3)
    code.add("var sql =", 3)
    code.add(f"{textwrap.indent(get_query_delete(table), '    ' * 4)};")
    code.add(f"var result = await db.ExecuteAsync(sql, new {{ {', '.join(keys)} }});", 3)
    code.add("return result > 0;", 3)
    code.add("}", 2)
    code.add("")

    code.add("}", 1)
    code.add("}")

    return code.get_code()
