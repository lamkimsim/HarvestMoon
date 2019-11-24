import sqlalchemy
import mysql


db_user = 'root'
db_pass = 'HarvestMoon'
db_name = 'farm_sensors'
cloud_sql_connection_name = 'harvestmoon:asia-east2:farmsensors'

db = sqlalchemy.create_engine(
    # Equivalent URL:
    # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=/cloudsql/<cloud_sql_instance_name>
    sqlalchemy.engine.url.URL(
        drivername='mysql+pymysql',
        username=db_user,
        password=db_pass,
        database=db_name,
        query={
            'unix_socket': '/cloudsql/{}'.format(cloud_sql_connection_name)
        }
    ),
    pool_size=5,
    max_overflow=2,
    pool_timeout=30,  # 30 seconds
    pool_recycle=1800,  # 30 minutes
)

