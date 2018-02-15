import argparse
from collect import collect_from_services



if __name__ == '__main__':

    # Services identified as potentially costly
    services_required = ['ec2', 'ec2_ebs']

    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--output", required=False, help="Path to the written report (CSV file)")
    ap.add_argument("--region", required=False, help="The region to use. Overrides config/env settings.")
    #ap.add_argument("--all", required=False, help="Return info about all services listed in variable services (currently only EC2)")
    #ap.add_argument("-v", "--verbose", required=False, help="Show info on terminal")
    args = vars(ap.parse_args())
    region = args["region"]
    collected = collect_from_services(services_required,region)

    if collected is not None:
        if args["output"]:
            with open(args["output"], 'w') as fout:
                collected.to_csv(fout)

        #if "verbose" in args:
        print(collected.head())

    else:
        print("No info was collected.")

