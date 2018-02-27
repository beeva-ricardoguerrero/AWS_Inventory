import pandas as pd

from EC2 import EC2
from S3 import S3


def collect_from_services(services_required,region):
    results = []
    if 'ec2' in services_required:
        ec2 = EC2(region)
        resources = ec2.collect()
        if len(resources):
            results.append(resources)

    if 's3' in services_required:
        s3 = S3(region)
        resources = s3.collect()
		
        if len(resources):
            results.append(resources)

    if results:
        return pd.concat(results)
    else:
        return None

