import boto3
from botocore.exceptions import ClientError
import pandas as pd

class EC2():

    def __init__(self,region):
        if region:
            boto3.setup_default_session(region_name=region)

        self.ec2 = boto3.client('ec2')
        self.FIELDS = ['Resource_Type', 'Description', 'ID', 'Status', 'Tag_name', 'Tag_project', 'Creation_date']
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
        i = self.collect_instances()
        v = self.collect_volumes()
        r = self.collect_reserved_instances()
        s = self.collect_snapshots()
        a = self.collect_addresses()
        
        return pd.concat([i,v,r,s,a])

    def collect_instances(self):
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
                            item_info['Tag_name'] = tag['Value']
                        if tag['Key'] == 'Project':
                            item_info['Tag_project'] = tag['Value']

                formatted_list.append(item_info)

        pruned = pd.DataFrame(formatted_list)
        
        return pruned

    def collect_volumes(self):
        try:
            response = self.ec2.describe_volumes()
        except ClientError as e:
            print("Exception in class " + self.__class__.__name__)
            print(e.message)
            return None

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
                        item_info['Tag_name'] = tag['Value']
                    if tag['Key'] == 'Project':
                        item_info['Tag_project'] = tag['Value']

            formatted_list.append(item_info)

        pruned = pd.DataFrame(formatted_list)

        return pruned

    def collect_spot_requests(self):
        try:
            response = self.ec2.describe_spot_instance_requests()
        except ClientError as e:
            print("Exception in class " + self.__class__.__name__)
            print(e.message)
            return None

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
                        item_info['Tag_name'] = tag['Value']
                    if tag['Key'] == 'Project':
                        item_info['Tag_project'] = tag['Value']

            formatted_list.append(item_info)

        pruned = pd.DataFrame(formatted_list)

        return pruned

    def collect_reserved_instances(self):
        try:
            response = self.ec2.describe_reserved_instances()
        except ClientError as e:
            print("Exception in class " + self.__class__.__name__)
            print(e.message)
            return None

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
        try:
            response = self.ec2.describe_snapshots()
        except ClientError as e:
            print("Exception in class " + self.__class__.__name__)
            print(e.message)
            return None

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
                        item_info['Tag_name'] = tag['Value']
                    if tag['Key'] == 'Project':
                        item_info['Tag_project'] = tag['Value']

            formatted_list.append(item_info)

        pruned = pd.DataFrame(formatted_list)

        return pruned

    def collect_addresses(self):
        try:
            response = self.ec2.describe_addresses()
        except ClientError as e:
            print("Exception in class " + self.__class__.__name__)
            print(e.message)
            return None

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
                        item_info['Tag_name'] = tag['Value']
                    if tag['Key'] == 'Project':
                        item_info['Tag_project'] = tag['Value']

            formatted_list.append(item_info)

        pruned = pd.DataFrame(formatted_list)

        return pruned

