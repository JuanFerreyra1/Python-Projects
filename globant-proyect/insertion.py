
from pyspark.sql import SparkSession
#lectura


def set_up():
  spark = SparkSession.builder.master("local[1]")\
  .appName("Insertion")\
  .config('spark.executors.cores', '4')\
  .getOrCreate()

def reading():
  #dataframe de spark
  df = spark.read.csv("hired_employees.csv",header=True)
  df.show(truncate=False)


def writing():
  #ingesta a la base de datos mysql
  df.write.format('jdbc').options(
        url='jdbc:mysql://localhost/globant',
        driver='com.mysql.jdbc.Driver',
        dbtable='Hired_employees',
        user='root',
        password='root').mode('append').save()


'''
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", help='username')
    parser.add_argument("--password", help='password')
    parser.add_argument("--dbname", help='mysql dbname')
    parser.add_argument("--dbtable", help='mysql db's table')
    parser.add_argument("--csvfilename", help='csv file to be inserted')
    

    args = parser.parse_args()
    user = args.username
    pass = args.password 
	dbname = args.dbname
	dbtable = args.dbtable
	csvfilename = args.csvfilename



    if not args.username:
        raise Exception(Missing  parameter: --username")
    if not args.password:
        raise Exception("Missing  parameter: --password")
    if not args.dbname:
        raise Exception(Missing  parameter: --dbname")
    if not args.dbtable:
        raise Exception("Missing  parameter --dbtable")
    if not args.csvfilename:
        raise Exception("Missing  parameter --csvfilename")

 '''



##########################################
#add security authentication
#associate script with dockerfile

#arguments --userid --password --dbname --dbtable --csvfilename 