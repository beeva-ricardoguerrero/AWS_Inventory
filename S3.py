import boto3
from botocore.exceptions import ClientError
import pandas as pd

class S3():
    def _aws_exception_handling(self, func):
        def __aws_exception_handling(*args, **kwargs):
            try:
                response = func()
                return response
            except ClientError as e:
                print("Exception in class " + self.__class__.__name__)
                print(e.message)
                return None
        return __aws_exception_handling

    def __init__(self, region):
        if region:
            boto3.setup_default_session(region_name=region)

        self.s3 = boto3.client('s3')
        self.FIELDS = ['Resource_Type', 'Name', 'Creation_date']

    def collect(self):
        # TODO public/private buckets
        response = self._aws_exception_handling(self.s3.list_buckets)()

        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            return None

        formatted_list = []

        for bucket in response['Buckets']:
            item_info = dict.fromkeys(self.FIELDS)
            item_info['Resource_Type'] = "S3 Bucket"
            item_info['Name'] = bucket['Name']
            item_info['Creation_date'] = bucket['CreationDate']

            formatted_list.append(item_info)

        pruned = pd.DataFrame(formatted_list)

        return pruned

