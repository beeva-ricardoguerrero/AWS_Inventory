# AWS_Inventory

simple tool to get an inventory of AWS resources

## usage

```
python main.py --region REGION --output {tab|csv}
```

## requirements
* python2
* pandas
* boto3
* tabulate

## TODO/BUGS

* -f option to write to a file ( -f file.csv, -f - to use stdout)
* S3 buckets are common to all regions
* Dockerfile

