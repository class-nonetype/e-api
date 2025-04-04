import sqlalchemy.orm


# Crea una clase base para las definiciones de clases declarativas de SQLAlchemy.
# Las clases declarativas en SQLAlchemy definen el mapeo entre las tablas de la base de datos 
# y las clases de Python, lo que permite realizar operaciones de base de datos a través de objetos (ORM).
base = sqlalchemy.orm.declarative_base()
