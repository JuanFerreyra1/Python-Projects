import argparse
import requests
import json
import boto3
import platform
import re

class Structure():
    def __init__(self,user,password,dag,date):
        self.user = user
        self.password = password
        self.dag = dag
        self.date = date.split(',')


    def get_structure(self):

        base_url = "hidden"

        def getToken(username,password):
            url = base_url+"auth/token/"
            session = requests.Session()
            session.auth = (username, password)    
            try:
                request = session.get(url, verify=False).json()
                token = request["token"]
                return token
            except:
                raise Exception("\x1b[1;31m"+"Failed to get token. Check if you are connected through hidden")

        self.token = getToken(self.user,self.password)

        url = base_url+"hidden"
        headers={'Content-type':'application/json', 'Accept':'application/json','Authorization':self.token}


        fullUrl = url+self.dag+'/'+self.date[0]

        try:
            request = requests.get(fullUrl, headers=headers, verify=False)
        except:
            raise Exception("DAG invalid")


        response = json.loads(request.text)
        dags_list = []
        dags_list.append(self.dag)
        dags_list_2 = response.get('hidden')
        try:
            for x in dags_list_2:
                dags_list.append(x)
        except:
            pass

        final_input = []
        dag_par  = []

        for y in self.date:
            for x in dags_list:
                dag_par = [x,y]
                final_input.append(dag_par)
            
        return final_input,self.token