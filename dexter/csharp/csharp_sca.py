from dexter.csharp.model_template import get_template as get_model_template
from dexter.csharp.irepository_template import get_template as get_irepository_template
from dexter.csharp.repository_template import get_template as get_repository_template
from dexter.csharp.sqlserver_template import get_template as get_sqlserver_repository_template
from dexter.csharp.postgresql_template import get_template as get_postgresql_repository_template
from io import open
import os


class CsharpSca:

    __tables = None
    __models_namespace = ""
    __repositories_namespace = ""
    __output_path = None

    def __init__(self, tables, models_namespace, repositories_namespace, output_path):
        self.__tables = tables
        self.__models_namespace = models_namespace
        self.__repositories_namespace = repositories_namespace
        self.__output_path = output_path

    def create_models(self):
        path = f"{self.__output_path}/Models"
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)
        for table in self.__tables:
            file = open(f"{path}/{table['name']}.cs", "w")
            file.write(get_model_template(table, self.__models_namespace))
            file.close()

    def create_interfaces(self):
        path = f"{self.__output_path}/Repositories"
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)
        for table in self.__tables:
            file = open(f"{path}/I{table['name']}Repository.cs", "w")
            file.write(get_irepository_template(table, self.__models_namespace, self.__repositories_namespace))
            file.close()

    def create_sqlserver_repository(self, connection_string):
        path = f"{self.__output_path}/Repositories"
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)
        file = open(f"{path}/GenericRepository.cs", "w")
        file.write(get_sqlserver_repository_template(self.__repositories_namespace, connection_string))
        file.close()

    def create_postgresql_repository(self, connection_string):
        path = f"{self.__output_path}/Repositories"
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)
        file = open(f"{path}/GenericRepository.cs", "w")
        file.write(get_postgresql_repository_template(self.__repositories_namespace, connection_string))
        file.close()

    def create_repositories(self):
        path = f"{self.__output_path}/Repositories"
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)
        for table in self.__tables:
            file = open(f"{path}/{table['name']}Repository.cs", "w")
            file.write(get_repository_template(table, self.__models_namespace, self.__repositories_namespace))
            file.close()
