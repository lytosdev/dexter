from dexter.csharp.csharp_sca import CsharpSca
from dexter.sqlserver.sqlserver_dbinfo import SqlServerDbInfo
from dexter.postgresql.postgresql_dbinfo import PostgreSqlDbInfo
import click
import json


@click.group()
def main():
    pass


def validate_language(ctx, param, value):
    language = str(value).lower()
    if language != "c#":
        raise click.BadParameter(f"Invalid {param}: {value}")
    else:
        return language


def validate_dbservice(ctx, param, value):
    dbservice = str(value).lower()
    if dbservice != "sqlserver":
        raise click.BadParameter(f"Invalid {param}: {value}")
    else:
        return dbservice


@main.command()
@click.argument("language", callback=validate_language)
@click.argument("dbservice", callback=validate_dbservice)
@click.option("--server", "-s")
@click.option("--database", "-d")
@click.option("--user", "-u")
@click.option("--password", "-p")
@click.option("--driver")
@click.option("--port")
@click.option("--dbconfig", "-c", type=click.Path(exists=True))
@click.option('--outputpath', "-o", default=".", type=click.Path(exists=True))
def create_sca(language, dbservice, server, database, user, password, driver, port, dbconfig, outputpath):

    info = None

    if dbconfig:
        dbconfig_file = open(f"{dbconfig}\dbconfig.json")
        dbconfig_data = json.load(dbconfig_file)
        server = dbconfig_data["server"]
        database = dbconfig_data["database"]
        user = dbconfig_data["user"]
        password = dbconfig_data["password"]
        driver = dbconfig_data["driver"]
        port = dbconfig_data["port"]
        dbconfig_file.close()

    if dbservice == "sqlserver":
        if not port:
            port = "1433"
        server = f"{server},{port}"
        info = SqlServerDbInfo(driver, server, database, user, password)
    elif dbservice == "postgresql":
        if not port:
            port = "5432"
        info = PostgreSqlDbInfo(server, port, database, user, password)

    info_db = info.get_info()

    if info_db:
        if language == "c#":
            models_namespace = click.prompt("Enter a name for the models namespace")
            repositories_namespace = click.prompt("Enter a name for the repositories namespace")
            csharp_sca = CsharpSca(info_db, models_namespace, repositories_namespace, outputpath)
            csharp_sca.create_models()
            csharp_sca.create_interfaces()
            if dbservice == "sqlserver":
                connection_string = f"Server={server},{port};Database={database};User Id={user};Password={password};"
                csharp_sca.create_sqlserver_repository(connection_string)
            elif dbservice == "postgresql":
                connection_string = f"Server={server};Port={port};Database={database};User Id={user};Password={password};"
                csharp_sca.create_postgresql_repository(connection_string)
            csharp_sca.create_repositories()
