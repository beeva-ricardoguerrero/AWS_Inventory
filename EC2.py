import boto3
from botocore.exceptions import ClientError
import pandas as pd

class EC2():

    def __init__(self,region):
        if region:
            boto3.setup_default_session(region_name=region)

        self.ec2 = boto3.client('ec2')
        self.FIELDS = ['Description', 'ID', 'Status', 'Tag_name', 'Tag_project', 'Creation_date']
        # TODO This is temporary, it should come in a base class

        # TODO check if the connection was established


    def collect(self, services=[]):
        """
        Get EC2 stuff

            Parameters
            ----------
            services: list
            It contains the interesting services in EC2 such as machines, spot instances, ebs and so on.
            If empty, means all services

            Returns: pandas' Dataframe
        """
        try:
            response = self.ec2.describe_instances()
        except ClientError as e:
            print("Exception in class " + self.__class__.__name__)
            print(e.message)

            return None

        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            return None

        # Pruning and formatting
        formatted_list = []

        print("Processing %d elements." % len(response['Reservations']) )

        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                item_info = dict.fromkeys(self.FIELDS)
                item_info['Description'] = instance['InstanceType']
                item_info['Creation_date'] = str(instance['LaunchTime']).split(" ")[0]
                item_info['ID'] = instance['InstanceId']
                item_info['Status'] = instance['State']['Name']
                if 'Tags' in instance:
                    for tag in instance['Tags']:
                        if tag['Key'] == 'Name':
                            item_info['Tag_name'] = tag['Value']
                        if tag['Key'] == 'Project':
                            item_info['Tag_project'] = tag['Value']

                formatted_list.append(item_info)

        pruned = pd.DataFrame(formatted_list)

        return pruned

