# from pyspark import SparkContext

# sc = SparkContext("local", "WordCount")
# txt = "PySpark makes big data processing fast and easy with Python"
# rdd = sc.parallelize([txt])

# counts = rdd.flatMap(lambda x: x.split()) \
#             .map(lambda word: (word, 1)) \
#             .reduceByKey(lambda a, b: a + b)

# print(counts.collect())
# sc.stop()


from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.tuning import ParamGridBuilder

# Initialize Spark session
spark = SparkSession.builder \
    .appName("LogisticRegressionExample") \
    .master("local[*]") \
    .getOrCreate()

lr = LogisticRegression()

output = ParamGridBuilder() \
    .baseOn({lr.labelCol: 'l'}) \
    .baseOn([lr.predictionCol, 'p']) \
    .addGrid(lr.regParam, [1.0, 2.0]) \
    .addGrid(lr.maxIter, [1, 5]) \
    .build()

print(output)

# Stop the Spark session
spark.stop()