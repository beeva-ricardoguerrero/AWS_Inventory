#!/usr/bin/env python
import argparse
from collect import collect_from_services
from tabulate import tabulate



if __name__ == '__main__':

    # Services identified as potentially costly
    services_required = ['ec2', 's3']

    ap = argparse.ArgumentParser()
    ap.add_argument("-o","--output", required=False, choices=['tab','csv'], help="output type", default='tab')
    ap.add_argument("--region", required=False, help="The region to use. Overrides config/env settings.")
    #ap.add_argument("--all", required=False, help="Return info about all services listed in variable services (currently only EC2)")
    #ap.add_argument("-v", "--verbose", required=False, help="Show info on terminal")
    args = vars(ap.parse_args())
    region = args["region"]
    collected = collect_from_services(services_required,region)

    if collected is None:
        print("no info was collected")
        exit(0)

    if args["output"] == "tab":
        print tabulate(collected, showindex='never', headers='keys', tablefmt='psql')
    else:
        print(collected.to_csv())

   