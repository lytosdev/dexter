def get_query_selectall(table):

    list_fields = [f"    {item['name']} AS {{nameof({table['name']}.{item['name']})}}" for item in table["fields"]]
    fields = ",\n".join(list_fields)

    return f"$@\"SELECT\n{fields}\nFROM {table['name']}\""


def get_query_selectbyid(table):

    list_fields = [f"    {item['name']} AS {{nameof({table['name']}.{item['name']})}}" for item in table["fields"]]
    fields = ",\n".join(list_fields)

    list_where = [f"{item['name']}=@{item['name']}" for item in table["fields"] if item["isPrimaryKey"] == 1]
    where = " AND ".join(list_where)

    return f"$@\"SELECT\n{fields}\nFROM {table['name']}\nWHERE {where}\""


def get_query_insert(table):

    list_fields = [item["name"] for item in table["fields"]
                   if item["dataType"] != "rowversion" and item["isIdentity"] == 0]
    fields = ", ".join(list_fields)

    list_values = [f"@{item['name']}" for item in table["fields"]
                   if item["dataType"] != "rowversion" and item["isIdentity"] == 0]
    values = ", ".join(list_values)

    return f"@\"INSERT INTO {table['name']}\n    ({fields})\n    VALUES\n    ({values})\""


def get_query_update(table):

    list_fields = [f"{item['name']}=@{item['name']}" for item in table["fields"]
                   if item["dataType"] != "rowversion" and item["isIdentity"] == 0]
    fields = ", ".join(list_fields)

    list_where = [f"{item['name']}=@{item['name']}" for item in table["fields"] if item["isPrimaryKey"] == 1]
    where = " AND ".join(list_where)

    return f"@\"UPDATE {table['name']}\nSET {fields}\nWHERE {where}\""


def get_query_delete(table):

    list_where = [f"{item['name']}=@{item['name']}" for item in table["fields"] if item["isPrimaryKey"] == 1]
    where = " AND ".join(list_where)

    return f"@\"DELETE FROM {table['name']}\nWHERE {where}\""
