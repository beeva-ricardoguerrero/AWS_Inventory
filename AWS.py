import boto3
from botocore.exceptions import ClientError

class AWS():
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

    def __init__(self, region=None):
        boto3.setup_default_session(region_name=region)
        self.region = region
        self.FIELDS = ['Resource_Type', 'Description', 'ID', 'Status', 'Name', 'Project', 'Creation_date']
