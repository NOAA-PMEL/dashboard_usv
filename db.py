import constants
import pandas as pd
import datetime
from sqlalchemy import text, Table, MetaData


def get_locations():
    # In this function, we retrieve the data from postgres using pandas's read_sql method.

    # This data is periodically getting updated via a separate Celery Process in tasks.py.
    # "dataset_table" is the name of the table that we initialized in tasks.py.

    updated_df = pd.read_sql(
        "SELECT * FROM {};".format(constants.locations_table), constants.postgres_engine
    )
    return updated_df

def get_mission_locations(mission_id, dsg_id):
    # In this function, we retrieve the data from postgres using pandas's read_sql method.

    # This data is periodically getting updated via a separate Celery Process in tasks.py.
    # "dataset_table" is the name of the table that we initialized in tasks.py.
    updated_df = pd.read_sql(
        "SELECT * FROM {} WHERE MISSION_ID=\'{}\' ORDER BY time,trajectory;".format(constants.locations_table, mission_id, dsg_id), constants.postgres_engine
    )
    return updated_df

def get_mission_locations_notsorted(mission_id):
    # In this function, we retrieve the data from postgres using pandas's read_sql method.

    # This data is periodically getting updated via a separate Celery Process in tasks.py.
    # "dataset_table" is the name of the table that we initialized in tasks.py.
    query = "SELECT * FROM {} WHERE MISSION_ID=\'{}\' ORDER BY TIME;".format(constants.locations_table, mission_id)
    print(query)
    updated_df = pd.read_sql(
        query, constants.postgres_engine
    )
    return updated_df


def delete_ds_drones(mid):
    dq = f"DELETE FROM {constants.locations_table} WHERE mission_id='{mid}'"
    print(dq)
    with constants.postgres_engine.connect() as conn:
        conn.execute(text(dq))
        conn.commit()


def drop():
    "DROP {}".format(constants.locations_table)