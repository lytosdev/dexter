# Dexter

## App de línea de comandos

A partir de una base de datos crea repositorios automáticamente para las operaciones CRUD

# Documentación

## Inicio

Por el momento sólo está disponible el scaffolding para C# con bases de datos SQL Server y PostgreSQL (haciendo uso de la librería dapper).

```console
> dexter create-sca c# sqlserver --driver=DRIVER -s=SERVER -d=DATABASE -u=USER -p=PASSWORD
```

En vez de pasar los parámetro de conexión uno por uno, puedes crear un archivo llamado dbconfig.json e indicar la ruta.

_dbconfig.json_

```json
{
    "driver": "DRIVER",
    "server": "SERVER",
    "port": "PORT",
    "database": "DATABASE",
    "user": "USER",
    "password": "PASSWORD"
}
```

```console
> dexter create-sca c# sqlserver -c "c:\dbconfig.json"
```

La ruta por defecto donde se generarán los repositorios es la ruta raíz pero se puede cambiar con la opción output -o

Por ejemplo, dada una base de datos con una tabla llamada Articulos y otra Clientes se generarán los siguientes archivos:

```
\Models
    Articulos.cs
    Clientes.cs
\Repositories
    ArticulosRepository.cs
    ClientesRepository.cs
    GenericRepository.cs
    ArticulosRepository.cs
    ClientesRepository.cs
```
