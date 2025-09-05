#!python
# Copyright (c) 2024 Eric Hoy
# Licensed under the MIT License

import boto3
from datetime import datetime
from tabulate import tabulate
from botocore.exceptions import ClientError

# Initialize AWS clients
ec2_client = boto3.client('ec2')

# Get the current date in the same format as the backup date
current_date = datetime.utcnow().strftime("%Y-%m-%d")

# List of all AWS regions
regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

# Function to process each VM
def process_vm(resource_arn, resource_name, backup_client, resourcegroupstaggingapi_client, vm_details, identified_issues):
    # Get the tags of the virtual machine using the Resource Groups Tagging API
    tags_response = resourcegroupstaggingapi_client.get_resources(
        ResourceARNList=[resource_arn]
    )
    tags = tags_response['ResourceTagMappingList'][0].get('Tags', [])
    tags_dict = {tag['Key']: tag['Value'] for tag in tags}

    # Get the last backup date 
    last_backup = None
    response = backup_client.list_backup_jobs(
        ByResourceArn=resource_arn,
        ByState='COMPLETED'
    )
    if response['BackupJobs']:
        last_backup = max(job['CompletionDate'] for job in response['BackupJobs']).strftime("%Y-%m-%d")

    if not last_backup:
        last_backup = "None"

    # Append the VM details to the list
    vm_details.append([
        resource_name.replace(" ", "_"),
        last_backup,
        tags_dict.get("Owner", "N/A"),
        tags_dict.get("Backup", "N/A"),
        tags_dict.get("aws:backup-gateway:path", "N/A")
    ])

    # Check for identified issues
    path = tags_dict.get("aws:backup-gateway:path", "")
    if path.startswith("/1155/vm/Production") and (last_backup == "None" or last_backup != current_date):
        identified_issues.append([resource_name.replace(" ", "_"), last_backup])

# Loop through each region
for region in regions:
    print("Processing region: " + region)
    
    # Set the AWS region for each client
    backup_gateway_client = boto3.client('backup-gateway', region_name=region)
    backup_client = boto3.client('backup', region_name=region)
    resourcegroupstaggingapi_client = boto3.client('resourcegroupstaggingapi', region_name=region)
    
    try:
        # List all virtual machines using AWS Backup Gateway
        all_vms = backup_gateway_client.list_virtual_machines()['VirtualMachines']
    except ClientError as e:
        if e.response['Error']['Code'] == 'AccessDeniedException':
            print(f"We do not have access to region: {region}. Skipping...")
            continue
        else:
            raise

    # Check if all_vms in the region is empty
    if not all_vms:
        print("No virtual machines found in " + region + ".")
        continue

    # List all AWS Backup Gateway VMs and their last seen time
    print("Backup Gateway VMs should be reporting with a current LastSeenTime:")
    gateways = backup_gateway_client.list_gateways()['Gateways']
    gateway_table = [[gateway['GatewayDisplayName'], gateway['LastSeenTime']] for gateway in gateways]
    print(tabulate(gateway_table, headers=["Gateway Name", "Last Seen Time"], tablefmt="grid"))

    # Initialize a list to store VM details and identified issues
    vm_details = []
    identified_issues = []

    # Process each VM
    for vm in all_vms:
        resource_arn = vm['ResourceArn']
        resource_name = vm['Name']
        process_vm(resource_arn, resource_name, backup_client, resourcegroupstaggingapi_client, vm_details, identified_issues)

    # Sort vm_details by Backup, Last Backup Date, and VM Name
    vm_details.sort(key=lambda x: (-int(x[3]) if x[3].isdigit() else float('-inf'), x[1], x[0]))

    # Print VM details in tabular format
    print("\n-----------------------------------------------------\n")
    print(tabulate(vm_details, headers=["VM Name", "Last Backup Date", "Owner", "Backup", "aws-backup-gateway:path"], tablefmt="grid"))

    # Print identified issues in tabular format
    print("\n-----------------------------------------------------\n")
    if identified_issues:
        print("PROBLEM! The following VMs are not being backed up:")
        print(tabulate(identified_issues, headers=["VM Name", "Last Backup Date"], tablefmt="grid"))
    else:
        print("All VMs in production paths in vSphere have current backups.")
    print("\n-----------------------------------------------------\n")
    print("\n-----------------------------------------------------\n")
    print("\n-----------------------------------------------------\n")