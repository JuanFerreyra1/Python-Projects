import argparse
import requests
import json
import boto3
import platform
import re
from Classifiers import *
from Airflow import *
from S3 import *
from Structure import *


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--hidden", help='hidden')
    parser.add_argument("--hidden", help='hidden')
    parser.add_argument("--hidden", help='hidden')
    parser.add_argument("--hidden", help='hidden')
    args = parser.parse_args()


    if not args.hidden:
        raise Exception("\x1b[1;31m"+"hidden")

    if not args.hidden:
        raise Exception("\x1b[1;31m"+"hidden")

    if not args.hidden:
        raise Exception("\x1b[1;31m"+"hidden")

    if not args.hidden:
        raise Exception("\x1b[1;31m"+"hidden")


    #structure
    structure_class= Structure(args.hidden,args.hidden,args.hidden,args.hidden)
    structure_to_check_tuple = structure_class.get_structure()
    structure_to_check = structure_to_check_tuple[0]
    token = structure_to_check_tuple[1]

    #credentials
    def connection_keys_aws():
        def set_config_path():
            os_platform = platform.system()
            path = ""
            if os_platform == "Windows":
                path = "C:\\Users\\{}\\.aws".format(args.hidden)
            elif os_platform == "Linux":
                path = "/home/{}/.aws".format(args.hidden)
            return path

        with open('{}/credentials'.format(set_config_path())) as f:
            lines = f.read()
        access_key = re.search("(?<=aws_access_key_id=).*",lines)[0]
        secret_access_key = re.search("(?<=aws_secret_access_key=).*",lines)[0]
        session_token =re.search("(?<=aws_session_token=).*",lines)[0]

        credentials = [access_key,secret_access_key,session_token]

        return credentials
    aws_local_credentials = connection_keys_aws()

    for x in structure_to_check:
        if x[0] == args.hidden:
            print("\x1b[1;30m"+"####################################################################################################################################################################################################")
            print("\x1b[1;30m"+"####################################################################################################################################################################################################")
            print("\x1b[1;30m"+"Date: {}".format(x[1]))
            print('\n')
        default_airflow_connection = Airflow_connection(x[0],x[1],args.hidden)
        airflow_result = default_airflow_connection.request_date()
        default_s3_connection = S3_connection(x[0],x[1],args.hidden,aws_local_credentials[0],aws_local_credentials[1],aws_local_credentials[2])
        s3_result_datalake = default_s3_connection.request_partition_data_lake()
        default_classifier_connection = Classifiers_connection(token,x[0],x[1])
        classifier_result = default_classifier_connection.request_classifier()
        s3_result_data_in = default_s3_connection.request_partition_data_in(airflow_result,s3_result_datalake,classifier_result,x[0])


        print(airflow_result)
        print(s3_result_datalake)
        print(classifier_result)
        print(s3_result_data_in)
        print('\n')

main()



