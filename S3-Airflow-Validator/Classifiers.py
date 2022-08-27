import argparse
import requests
import json
import boto3
import platform
import re

class Classifiers_connection:
    def __init__(self,token,dag,date):
        self.token = token
        self.dag = dag
        self.date = date


    def request_classifier(self):   
        base_url = "hidden"
        url = base_url+"hidden"
        headers={'Content-type':'application/json', 'Accept':'application/json','Authorization':self.token}
        fullUrl = url+self.dag+'/'+self.date
        final_answer = str()
        try:
            if 'hidden' not in self.dag:
                request = requests.get(fullUrl, headers=headers, verify=False)
                response= json.loads(request.text).get("hidden")
                if len(response)==0:
                    final_answer = "\x1b[1;32m"+"   hidden-> {} ran ok".format(json.loads(request.text).get('hidden')[0])
                else:
                    final_answer = "\x1b[1;31m"+"   hidden-> {} didn't run ok".format(json.loads(request.text).get('hidden')[0])
            else:
                final_answer = "\x1b[1;32m"+"   hidden-> No aplica"

        except:
            raise Exception("\x1b[1;31m"+"Invalid DAG: It can be happening because DAG is OFF on AIRFLOW or it doesn't exist.")

        return final_answer