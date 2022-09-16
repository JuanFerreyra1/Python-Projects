from pyspark.sql import SparkSession
import argparse
import avro.schema
import mysql.connector
import pyspark
from pyspark.sql.types import *



class Challenge_one():

  def __init__(self,username,password,database,dbtable,csv_filename):
    self.username = username
    self.password = password
    self.database = database
    self.dbtable  = dbtable
    self.csvfilename = csv_filename

  def set_up(self):
    self.spark = SparkSession.builder.master("local[1]")\
    .appName("Insertion")\
    .config('spark.executors.cores', '4')\
    .config("spark.speculation","false")\
    .getOrCreate()

  def reading(self):
    self.df = self.spark.read.csv("csv-files/{}".format(self.csvfilename),header=True)
    self.df_count = self.df.count()
    print("\n"+"\n")
    print("\x1b[1;30m"+"{} rows are going to be inserted on database {} - table {}".format(self.df_count,self.database,self.dbtable))
    self.df.show()
    print("\n"+"\n")

  def writing(self):
    print("\x1b[1;33m"+"Insertion starts...")
    self.df.write.format('jdbc').options(
          url='jdbc:mysql://localhost/{}'.format(self.database),
          driver='com.mysql.cj.jdbc.Driver',
          dbtable='{}'.format(self.dbtable),
          user='{}'.format(self.username),
          password='{}'.format(self.password)).mode('append').save()
    print("\x1b[1;32m"+"Insertion has finished succesfully"+"\x1b[1;30m"+"\n")


  def backup(self):
    print("\x1b[1;33m"+"Starting backup of table with all its data...")
    self.df_backup = self.spark.read.jdbc(url='jdbc:mysql://localhost/{}'.format(self.database),table='{}.{}'.format(self.database,self.dbtable),properties={"user":"{}".format(self.username),"password":"{}".format(self.password)})
    self.df_backup.write.format("avro").save("AVRO-backups/{}.avro".format(self.dbtable))
    print("\x1b[1;32m"+"Backup has finished succesfully"+"\x1b[1;30m"+"\n")

  def execute(self):
    #self.set_up()
    #self.reading()
    #self.writing()
    #self.backup()
    pass



def main():

  def authentication():  
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", help='username')
    parser.add_argument("--password", help='password')
    parser.add_argument("--dbname", help='mysql dbname')
    parser.add_argument("--dbtable", help='mysql dbs table')
    parser.add_argument("--csvfilename", help='csv file to be inserted')
     
    args = parser.parse_args()
    if not args.username:
        raise Exception("\x1b[1;31m"+"Missing  parameter: --username")
    if not args.password:
        raise Exception("\x1b[1;31m"+"Missing  parameter: --password")
    if not args.dbname:
        raise Exception("\x1b[1;31m"+"Missing  parameter: --dbname")
    if not args.dbtable:
        raise Exception("\x1b[1;31m"+"Missing  parameter --dbtable")
    if not args.csvfilename:
        raise Exception("\x1b[1;31m"+"Missing  parameter --csvfilename")     
    user = args.username
    password = args.password 
    dbname = args.dbname
    dbtable = args.dbtable
    csvfilename = args.csvfilename
    return user,password,dbname,dbtable,csvfilename



  challenge_one_object = Challenge_two(authentication()[0],authentication()[1],authentication()[2],authentication()[3],authentication()[4])
  challenge_one_object.execute()


main()



##########################################
#associate script with dockerfile

