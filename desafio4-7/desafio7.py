from pyspark.sql import SparkSession
from datetime import date
import os
from pyspark.sql.functions import rank
from pyspark.sql.window import Window
from pyspark.sql.functions import col, explode,monotonically_increasing_id

spark = SparkSession.builder.appName('pract').getOrCreate()
df_pyspark = spark.read.json('MPE1004.json')
df = df_pyspark.select(explode(col('results')))
df = df.withColumn('RowId', monotonically_increasing_id() + 1 )
df = df.selectExpr('RowId','col.id as itemId','col.sold_quantity','col.available_quantity')
visits_df = spark.read.option('header',True).csv('visits.csv')
df = df.join(visits_df,visits_df.itemId == df.itemId).select(df["*"],visits_df['visits'])
df = df.withColumn('stockPercentage', (col('available_quantity')*100)/(col('sold_quantity')+col('available_quantity')))
df.select('ItemId','available_quantity','stockPercentage').show(1000)