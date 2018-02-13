import boto3

from botocore.exceptions import ClientError

import pandas as pd


class EC2():

	def __init__(self):
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

		for item in response['Reservations']:

			item_info = dict.fromkeys(self.FIELDS)

			item_info['Description'] = item['Instances'][0]['InstanceType']
			item_info['Creation_date'] = item['Instances'][0]['LaunchTime']
			item_info['ID'] = item['Instances'][0]['InstanceId']
			item_info['Status'] = item['Instances'][0]['State']['Name']
			item_info['Tag_name'] = item['Instances'][0]['Tags'][0].get('Name', None)
			item_info['Tag_project'] = item['Instances'][0]['Tags'][0].get('Project', None)

			formatted_list.append(item_info)


		pruned = pd.DataFrame(formatted_list)

		return pruned