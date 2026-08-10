#!/usr/bin/env python3
"""
Example PySpark script connecting to containerized HDFS (hdfs://localhost:9000).
Demonstrates DataFrame creation, HDFS Parquet/CSV writes, and reads.
"""

try:
    from pyspark.sql import SparkSession
    from pyspark.sql.functions import col, avg, count
except ImportError:
    print("Error: PySpark is not installed. Install via: pip install pyspark")
    exit(1)

def main():
    print("=== 1. Initializing SparkSession with HDFS URI ===")
    spark = SparkSession.builder \
        .appName("HadoopDockerPySparkExample") \
        .master("local[*]") \
        .config("spark.hadoop.fs.defaultFS", "hdfs://localhost:9000") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    print("=== 2. Creating Sample Dataset ===")
    data = [
        ("Alice", "Engineering", 95000, "Cairo"),
        ("Bob", "Marketing", 68000, "Alexandria"),
        ("Charlie", "Engineering", 105000, "Giza"),
        ("Diana", "Data Science", 112000, "Cairo"),
        ("Evan", "Marketing", 72000, "Cairo"),
        ("Fiona", "Data Science", 120000, "Alexandria")
    ]
    columns = ["Name", "Department", "Salary", "City"]
    df = spark.createDataFrame(data, columns)
    
    print("\n--- Original DataFrame ---")
    df.show()

    hdfs_path = "hdfs://localhost:9000/data/spark_employees.parquet"

    print(f"=== 3. Writing DataFrame to HDFS as Parquet: {hdfs_path} ===")
    df.write.mode("overwrite").parquet(hdfs_path)

    print("=== 4. Reading Data back from HDFS ===")
    loaded_df = spark.read.parquet(hdfs_path)

    print("\n--- Department Salary Aggregations ---")
    agg_df = loaded_df.groupBy("Department").agg(
        count("Name").alias("EmployeeCount"),
        avg("Salary").alias("AverageSalary")
    )
    agg_df.show()

    spark.stop()
    print("=== PySpark HDFS Example Completed Successfully ===")

if __name__ == "__main__":
    main()
