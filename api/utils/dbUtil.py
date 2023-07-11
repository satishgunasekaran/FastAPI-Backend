import databases
import sqlalchemy
from functools import lru_cache
from api import config
from api.models import metadata
from starlette.config import Config

# Using Pydanctic to load environment variables

# @lru_cache()
# def setting():
#     return config.Settings()

# def database_psql_url_config():
#     return str(setting().DB_CONNECTION) + "://" + str(setting().DB_USERNAME) + ":" + str(setting().DB_PASSWORD) + "@" + str(setting().DB_HOST+":"+str(setting().DB_PORT) +
#         "/" + str(setting().DB_DATABASE)) 
    

# Using Starlette to connect to the database
def database_pgsql_url_config():
    conf = Config(".env")
    return str(conf("DB_CONNECTION") + "://" + conf("DB_USERNAME") + ":" + conf("DB_PASSWORD") + "@" + conf("DB_HOST")+":"+conf("DB_PORT") +   "/" + conf("DB_DATABASE"))

 

database = databases.Database(database_pgsql_url_config())
engine = sqlalchemy.create_engine(database_pgsql_url_config())

metadata.create_all(engine)





    



