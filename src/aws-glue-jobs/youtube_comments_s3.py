import sys
from datetime import datetime, timedelta
from typing import Any, List

import requests
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql import DataFrame
from pyspark.sql.functions import concat, sha2

from scraping.youtube_scrapping import main as youtube_data

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
logger = glueContext.get_logger()
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

def load_data_to_redshift(dyn_df: DynamicFrame, host: str, port: int, user: str, pwd: str, table: str,args, glueContext):
    redshift_conn_options = {
        "url": f"jdbc:redshift://{host}:{port}/{REDSHIFT_DATABASE_NAME}",
        "dbtable": table,
        "user": user,
        "password": pwd,
        "redshiftTmpDir": args["TempDir"],
    }

    glueContext.write_dynamic_frame.from_options(
        frame=dyn_df,
        connection_type="redshift",
        connection_options=redshift_conn_options,
    )

def main():
    data = youtube_data
    sdf = spark.createDataFrame(data)
    dyn_df = DynamicFrame.fromDF(sdf, glueContext, "dyn_df")
    
    load_data_to_redshift(
        dyn_df,
        redshift_secret["host"],
        redshift_secret["port"],
        redshift_secret["username"],
        redshift_secret["password"],
        "tablename",
        args,
        glueContext,
    )
    

if __name__ == "__main__":
    main()
    job.commit()