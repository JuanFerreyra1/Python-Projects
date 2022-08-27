import argparse
import requests
import json
import boto3
import platform
import re


class Airflow_connection:

        def __init__(self,received_dag,received_date,received_interface):
            self.dag = received_dag
            self.date = received_date
            if not '-' in self.date:
                self.date = self.date[0:4]+"-"+self.date[4:6]+"-"+self.date[6:8]
            self.interface = received_interface

        def request_date(self):
            headers = {"Authorization":"hidden","Content-type":"application/json"}
            primary_url = "hidden"
            completed_url = primary_url+'dags/{}/dagRuns?limit=30&order_by=-execution_date'.format(self.dag)

            request=requests.get(completed_url, headers=headers, verify=False)
            response=json.loads(request.text)
            response_list = response.get('dag_runs')
            if self.dag == self.interface:    
                self.final_answer = "\x1b[1;30m"+"DAG: {}".format(self.dag)+"\n"+"\x1b[1;31m"+"   Airflow: it didn't run on that date"
            else:
                self.final_answer = "\x1b[1;30m"+"   DEP: {}".format(self.dag)+"\n"+"\x1b[1;31m"+"   Airflow: it didn't run on that date"

            try:

                for x in response_list:
                    run_date = x.get('conf').get('date_from') 
                    run_state = x.get('state')
                    try:
                            if run_date == self.date and run_state == 'success':
                                self.execution_date  = x.get('execution_date')
                                self.start_date = x.get('start_date') 
                                self.end_date =  x.get('end_date')
                                self.state = run_state
                                if self.dag == self.interface:
                                    self.final_answer ="\x1b[1;30m"+"DAG: {}".format(self.dag)+"\n"+"\x1b[1;32m"+"   Airflow: start_date: {}   end_date: {}  execution_date: {}  state: {}".format(self.start_date,self.end_date,self.execution_date,self.state)
                                else:
                                    self.final_answer ="\x1b[1;30m"+"   DEP: {}".format(self.dag)+"\n"+"\x1b[1;32m"+"   Airflow: start_date: {}   end_date: {}  execution_date: {}  state: {}".format(self.start_date,self.end_date,self.execution_date,self.state)
                                break
                            if run_date == self.date and run_state == 'failed':
                                self.execution_date  = x.get('execution_date')
                                self.start_date = x.get('start_date') 
                                self.end_date =  x.get('end_date')
                                self.state = run_state
                                if self.dag == self.interface:
                                    self.final_answer ="\x1b[1;30m"+"DAG: {}".format(self.dag)+"\n"+"\x1b[1;31m"+"   Airflow: start_date: {}   end_date: {}  execution_date: {}  state: {}".format(self.start_date,self.end_date,self.execution_date,self.state)
                                else:
                                    self.final_answer ="\x1b[1;30m"+"   DEP: {}".format(self.dag)+"\n"+"\x1b[1;31m"+"   Airflow: start_date: {}   end_date: {}  execution_date: {}  state: {}".format(self.start_date,self.end_date,self.execution_date,self.state)
                                break
                            if run_date == self.date and run_state == 'running':
                                self.execution_date  = x.get('execution_date')
                                self.start_date = x.get('start_date') 
                                self.end_date =  x.get('end_date')
                                self.state = run_state
                                if self.dag == self.interface:
                                    self.final_answer ="\x1b[1;30m"+"DAG: {}".format(self.dag)+"\n"+"\x1b[1;33m"+"   Airflow: start_date: {}   end_date: {}  execution_date: {}  state: {}".format(self.start_date,self.end_date,self.execution_date,self.state)

                                else: 
                                    self.final_answer ="\x1b[1;30m"+"DEP: {}".format(self.dag)+"\n"+"\x1b[1;33m"+"   Airflow: start_date: {}   end_date: {}  execution_date: {}  state: {}".format(self.start_date,self.end_date,self.execution_date,self.state)                               
                                break
                    except:
                         break
            except:
                pass
            return self.final_answer