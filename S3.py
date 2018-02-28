import boto3
from botocore.exceptions import ClientError
import pandas as pd
from AWS import AWS

class S3(AWS):
    def __init__(self,region=None):
        AWS.__init__(self, region=region)
        self.s3 = boto3.client('s3')

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
            item_info['Creation_date'] = str(bucket['CreationDate']).split(" ")[0]
            
            formatted_list.append(item_info)

        pruned = pd.DataFrame(formatted_list)

        return pruned

