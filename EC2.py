import boto3
from botocore.exceptions import ClientError
import pandas as pd

class EC2():

    def _aws_exception_handling(self,func):
        def __aws_exception_handling(*args, **kwargs):
            try:
                response = func()
                return response
            except ClientError as e:
                print("Exception in class " + self.__class__.__name__)
                print(e.message)
                return None
        return __aws_exception_handling


    def __init__(self,region=None):
        boto3.setup_default_session(region_name=region)
        self.region = region
        self.ec2 = boto3.client('ec2')
        self.FIELDS = ['Resource_Type', 'Description', 'ID', 'Status', 'Name', 'Project', 'Creation_date']
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
        instances = self.collect_instances()
        vols = self.collect_volumes()
        reserved = self.collect_reserved_instances()
        snaps = self.collect_snapshots()
        addrs = self.collect_addresses()
        
        ret = pd.concat([instances,vols,reserved,snaps,addrs])
        return ret


    def collect_instances(self):

    	response = self._aws_exception_handling(self.ec2.describe_instances)()

        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            return None

        # Pruning and formatting
        formatted_list = []

        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                item_info = dict.fromkeys(self.FIELDS)
                item_info['Resource_Type'] = "instance"
                item_info['Description'] = instance['InstanceType']
                item_info['Creation_date'] = str(instance['LaunchTime']).split(" ")[0]
                item_info['ID'] = instance['InstanceId']
                item_info['Status'] = instance['State']['Name']
                if 'Tags' in instance:
                    for tag in instance['Tags']:
                        if tag['Key'] == 'Name':
                            item_info['Name'] = tag['Value']
                        if tag['Key'] == 'Project':
                            item_info['Project'] = tag['Value']

                formatted_list.append(item_info)

        pruned = pd.DataFrame(formatted_list)
        
        return pruned

    def collect_volumes(self):

    	response = self._aws_exception_handling(self.ec2.describe_volumes)()

        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            return None

        # Pruning and formatting
        formatted_list = []

        for volume in response['Volumes']:
            item_info = dict.fromkeys(self.FIELDS)
            item_info['Resource_Type'] = "ebs volume"
            item_info['Description'] = str(volume['Size']) + "G"
            item_info['Creation_date'] = str(volume['CreateTime']).split(" ")[0]
            item_info['ID'] = volume['VolumeId']
            item_info['Status'] = volume['State']
            if 'Tags' in volume:
                for tag in volume['Tags']:
                    if tag['Key'] == 'Name':
                        item_info['Name'] = tag['Value']
                    if tag['Key'] == 'Project':
                        item_info['Project'] = tag['Value']

            formatted_list.append(item_info)

        pruned = pd.DataFrame(formatted_list)

        return pruned

    def collect_spot_requests(self):

        response = self._aws_exception_handling(self.ec2.describe_spot_instance_requests)()

        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            return None

        # Pruning and formatting
        formatted_list = []

        for spotreq in response['SpotInstanceRequests']:
            item_info = dict.fromkeys(self.FIELDS)
            item_info['Resource_Type'] = "spot instance request"
            item_info['Description'] = spotreq['LaunchSpecification']['InstanceType']
            item_info['Creation_date'] = str(spotreq['CreateTime']).split(" ")[0]
            item_info['ID'] = spotreq['SpotInstanceRequestId']
            item_info['Status'] = spotreq['State']
            if 'Tags' in spotreq:
                for tag in spotreq['Tags']:
                    if tag['Key'] == 'Name':
                        item_info['Name'] = tag['Value']
                    if tag['Key'] == 'Project':
                        item_info['Project'] = tag['Value']

            formatted_list.append(item_info)

        pruned = pd.DataFrame(formatted_list)

        return pruned


    def collect_reserved_instances(self):

    	response = self._aws_exception_handling(self.ec2.describe_reserved_instances)()

        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            return None

        # Pruning and formatting
        formatted_list = []

        for instance in response['ReservedInstances']:
            item_info = dict.fromkeys(self.FIELDS)
            item_info['Resource_Type'] = "reserved instance"
            item_info['Description'] = instance['InstanceType']
            item_info['Creation_date'] = str(instance['Start']).split(" ")[0]
            item_info['ID'] = instance['ReservedInstancesId']
            item_info['Status'] = instance['State']

            formatted_list.append(item_info)

        pruned = pd.DataFrame(formatted_list)

        return pruned


    def collect_snapshots(self):

    	response = self._aws_exception_handling(self.ec2.describe_snapshots)()

        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            return None

        # Pruning and formatting
        formatted_list = []

        for snapshot in response['Snapshots']:
            item_info = dict.fromkeys(self.FIELDS)
            item_info['Resource_Type'] = "snapshot"
            item_info['Description'] = str(snapshot['VolumeSize']) + "G"
            item_info['Creation_date'] = str(snapshot['StartTime']).split(" ")[0]
            item_info['ID'] = snapshot['SnapshotId']
            item_info['Status'] = snapshot['State']
            if 'Tags' in snapshot:
                for tag in snapshot['Tags']:
                    if tag['Key'] == 'Name':
                        item_info['Name'] = tag['Value']
                    if tag['Key'] == 'Project':
                        item_info['Project'] = tag['Value']

            formatted_list.append(item_info)

        pruned = pd.DataFrame(formatted_list)

        return pruned


    def collect_addresses(self):

    	response = self._aws_exception_handling(self.ec2.describe_addresses)()

        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            return None

        # Pruning and formatting
        formatted_list = []

        for addr in response['Addresses']:
            item_info = dict.fromkeys(self.FIELDS)
            item_info['Resource_Type'] = "address"
            item_info['ID'] = addr['PublicIp']
            if 'Tags' in addr:
                for tag in addr['Tags']:
                    if tag['Key'] == 'Name':
                        item_info['Name'] = tag['Value']
                    if tag['Key'] == 'Project':
                        item_info['Project'] = tag['Value']

            formatted_list.append(item_info)

        pruned = pd.DataFrame(formatted_list)

        return pruned
