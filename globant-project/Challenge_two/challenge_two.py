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

      self.db_connection = mysql.connector.connect(user="root", password="root")
      self.db_cursor = self.db_connection.cursor(buffered=True)
      self.db_cursor.execute("use globant;")
      try:
        self.db_cursor.execute("drop view view_1;")
        self.db_cursor.execute("drop view view_2;")
      except:
        pass
      self.db_cursor.execute("""

      create view view_1 as (
      select x.*,QUARTER(x.datetime) as quarter from
      (
      select he.*,d.department,j.job from hired_employees as he 
      left join departments  as d on he.department_id=d.id 
      left join jobs as j on he.job_id = j.id
      )x
      )
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
      print("\n")

  def metrics_second_exercise(self):
    print("\n")
    print("""LIST OF IDS, NAME AND NUMBER OF EMPLOYEES HIRED OF EACH DEPARTMENT THAT HIRED MORE EMPLOYEES THAN THE MEAN OF EMPLOYEES HIRED IN 2021 FOR ALL THE DEPARTMENTS:""")
    self.db_connection = mysql.connector.connect(user="root", password="root")
    self.db_cursor = self.db_connection.cursor(buffered=True)
    self.db_cursor.execute("use globant;")
    try:
      self.db_cursor.execute("drop view employees_per_dept;")
      self.db_cursor.execute("drop view mean;")
    except:
      pass
    self.db_cursor.execute("""
        create view employees_per_dept as(

        select x.id_d,x.department,count(1) as employees 
        from 
        (
        select he.id,he.name,he.datetime,d.department,d.id as id_d,j.job from hired_employees as he 
        left join departments as d on he.department_id=d.id 
        left join jobs as j on he.job_id = j.id
        )x 
        where x.datetime between '2021-01-01' and '2021-12-31'
        group by x.id_d,x.department
        ) 
        ;
        """)
    self.db_cursor.execute("""
        create view mean as(
        select round(avg(employees),0) as value from employees_per_dept
        )
        ;
        """)
    self.db_cursor.execute("""

      select * from employees_per_dept where employees >(select value from mean)
      order by employees DESC;

      """)
    self.output_two = self.db_cursor.fetchall()
    self.columns_two = ["id", "department", "hired"]
    self.final_output_two = self.spark.createDataFrame(self.output_two,self.columns_two)
    self.final_output_two = self.final_output_two.select(
                         self.final_output_two.id.cast(IntegerType()),
                         self.final_output_two.department.cast(StringType()),
                         self.final_output_two.hired.cast(IntegerType()))
    print(self.final_output_two.show(truncate=False))    

  def execute(self):
    self.set_up()
    self.metrics_first_exercise()
    self.metrics_second_exercise()



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
