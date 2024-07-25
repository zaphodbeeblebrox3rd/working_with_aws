# AWS CLI Scripts

This directory contains a collection of scripts designed to interact with various AWS services using the AWS Command Line Interface (CLI). These scripts automate common tasks such as provisioning resources, managing configurations, and deploying applications.

## Prerequisites

Before using these scripts, ensure you have the following:

- **AWS CLI**: Installed and configured with the necessary permissions.
- **Python 3.6 or later**: Some scripts may require Python for additional processing.
- **Boto3 library for Python**: Required for scripts that interact with AWS services through Python.
- **AWS Credentials**: Most likely you will set your AWS environment variables.

Install the necessary Python dependencies by running:
```
pip install -r requirements.txt
```

## Scripts Overview


#### aws-backup-report.py

This script lists out the most recent AWS for vSphere backup jobs, their tags, and identifies production VMs that were not backed up.
It identifies production VMs on the basis of their path in vSphere.  There is a version for bash (aws-backup-report.sh) but it is not as pretty or fast as the python script.

```
./aws-backup-report.py
```


#### show-transcribe-job-tags.sh

This script produces a list of transcribe jobs with their tags.

```
./show-transcribe-job-tags.sh
```

Example Output:
> Job Name: transcribe_job_experiment_1, Creation Time: 2024-07-12T12:31:47.316000-05:00, Owner Tag: researcher1
> Job Name: transcribe_job_experiment_2, Creation Time: 2024-07-12T12:31:47.316000-05:00, Owner Tag: researcher2



### show-vpc-resources.sh
It can be very difficult to locate all resources in a VPC.
This script alleviates that pain somewhat by revealing all resources in a VPC, including subnets, security groups, and NAT gateways.

#### Usage
```
./show-vpc-resources.sh
```
