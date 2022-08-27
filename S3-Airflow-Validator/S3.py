import argparse
import requests
import json
import boto3
import platform
import re



class S3_connection:

    def __init__(self,received_dag,received_date,user,access_key,secret_access_key,session_token):
        self.dag = received_dag
        self.date = received_date
        if '-' in self.date:
            self.date = self.date [0:4]+self.date [5:7]+self.date [8:10]        
        self.user = user
        self.access_key = access_key
        self.secret_access_key = secret_access_key
        self.session_token = session_token
        def get_table(self):
            with open("final_dictionary.txt") as f:
                lines = f.read()
            self.path = str()
            try:
                self.input_dictionary = json.loads(lines)
                self.path = self.input_dictionary.get('{}'.format(self.dag))
            except:
                print("File dictionary.txt is null")
            return self.path
        self.path = get_table(self)
        





    def request_partition_data_in(self,airres,busres,clares,dag):
        self.airres = airres
        self.busres = busres
        self.clares = clares
        self.dag_id = dag
        self.final_answer = str()
        if 'hidden' not in self.dag_id:

            connection_session = boto3.Session(
                    aws_access_key_id = self.access_key,
                    aws_secret_access_key = self.secret_access_key,
                    aws_session_token =(self.session_token)
            )

            s3_client = connection_session.client('s3')
            file = re.search("(?<=\^).*(?=\(\()",self.path[2])[0]+self.date

            response = s3_client.list_objects(
                    Bucket="hidden",
                    Prefix="hidden/{}".format(file)
                    )

            if len(self.path[2])>1:
                if response.get("Contents") is None:
                    if "it didn't run" in self.airres and "it doesn't exist" in self.busres and "it didn't run" in self.clares:
                        self.final_answer = "\x1b[1;30m"+"   S3->hidden: File {}.* didn't arrived at location".format(file)          
                    else:
                        self.final_answer = "\x1b[1;30m"+"   S3->hidden: File {}.* isn't in the location".format(file)
                else:
                    self.final_answer = "\x1b[1;31m"+"   S3->hidden: File {}.*     is in the location".format(file)
            
            else:
                self.final_answer = "\x1b[1;31m"+"   Error: dictionary.txt null"
        else:
            self.final_answer ="\x1b[1;32m"+"   S3->hidden: it doesn't apply"
        
        return self.final_answer
        

    def request_partition_data_lake(self):

        connection_session = boto3.Session(
                aws_access_key_id = self.access_key,
                aws_secret_access_key = self.secret_access_key,
                aws_session_token =(self.session_token)
        )

        s3_client = connection_session.client('s3')


        response = s3_client.list_objects(
                Bucket="hidden",
                Prefix="{}/hidden={}/".format(self.path[0],self.date)
                )
        if len(self.path[0])>1:
            if response.get("Contents") is None:
                self.final_answer = "\x1b[1;31m"+"   S3->hidden: partition doesn't exist {}".format(self.date)
            else:
                self.final_answer = "\x1b[1;32m"+"   S3->hidden: partition exists {}".format(self.date)
        
        else:
            self.final_answer = "\x1b[1;31m"+"   Error: dictionary.txt invalid"
        
        return self.final_answer