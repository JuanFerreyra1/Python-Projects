from pyspark.sql import SparkSession
import argparse
import avro.schema
import mysql.connector
import pyspark
from pyspark.sql.types import *



class Challenge_two():

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

    
  def metrics_first_exercise(self):
      print("\n")
      print("NUMBER OF EMPLOYEES HIRED FOR EACH JOB AND DEPARTMENT IN 2021 DIVIDED BY QUARTER:")

      self.hired_employees = self.spark.read.jdbc(url='jdbc:mysql://localhost/{}'.format(self.database),table='{}.hired_employees'.format(self.database),properties={"user":"{}".format(self.username),"password":"{}".format(self.password)})
      self.departments = self.spark.read.jdbc(url='jdbc:mysql://localhost/{}'.format(self.database),table='{}.departments'.format(self.database),properties={"user":"{}".format(self.username),"password":"{}".format(self.password)})
      self.jobs = self.spark.read.jdbc(url='jdbc:mysql://localhost/{}'.format(self.database),table='{}.jobs'.format(self.database),properties={"user":"{}".format(self.username),"password":"{}".format(self.password)})
      self.parcial_join = self.hired_employees.join(self.departments,self.hired_employees.department_id == self.departments.id,how="left").drop(self.departments.id)
      self.final_join = self.parcial_join.join(self.jobs,self.parcial_join.job_id == self.jobs.id,how="left").drop(self.jobs.id)
      self.db_connection = mysql.connector.connect(user="root", password="root")
      self.db_cursor = self.db_connection.cursor(buffered=True)
      self.db_cursor.execute("use globant;")
      try:
        self.db_cursor.execute("drop view view_1;")
        self.db_cursor.execute("drop view view_2;")
      except:
        pass
      self.db_cursor.execute("""

      create view view_1 as
      select x.*,QUARTER(x.datetime) as quarter from
      (
      select he.*,d.department,j.job from hired_employees as he 
      left join departments  as d on he.department_id=d.id 
      left join jobs as j on he.job_id = j.id
      )x

      ;""")
      self.db_cursor.execute("""
        create view view_2 as(
      select view_1.*,
      case when quarter = '1' then 1 else 0 end as Q1,
      case when quarter = '2' then 1 else 0 end as Q2,
      case when quarter = '3' then 1 else 0 end as Q3,
      case when quarter = '4' then 1 else 0 end as Q4 
      from view_1
      )
      ;""")
      self.db_cursor.execute("""
      select department,job,sum(Q1) as Q1,sum(Q2) as Q2,sum(Q3) as Q3,sum(Q4) as Q4    
      from view_2 
      group by department,job
      order by department,job;
         """)
      self.output = self.db_cursor.fetchall()
      self.columns = ["department", "job", "Q1","Q2","Q3","Q4"]
      self.final_output = self.spark.createDataFrame(self.output,self.columns)
      self.final_output = self.final_output.select(
                         self.final_output.department.cast(StringType()),
                         self.final_output.job.cast(StringType()),
                         self.final_output.Q1.cast(IntegerType()),
                         self.final_output.Q2.cast(IntegerType()),
                         self.final_output.Q3.cast(IntegerType()),
                         self.final_output.Q4.cast(IntegerType()))

      print(self.final_output.show(truncate=False))


  def metrics_second_exercise(self):
    pass

  def execute(self):
    self.set_up()
    self.metrics_first_exercise()



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


  challenge_two_object = Challenge_two(authentication()[0],authentication()[1],authentication()[2],authentication()[3],authentication()[4])
  challenge_two_object.execute()


main()



##########################################
#associate script with dockerfile
