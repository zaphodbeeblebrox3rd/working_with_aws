#!/bin/bash
# Run a report of AWS Backups for vSphere VMs
# Author: Eric Hoy
# Date: 2024-07-11

# Get the current date in the same format as the backup date
current_date=$(date +"%Y-%m-%d")

# List all virtual machines using AWS Backup Gateway
all_vms=$(aws backup-gateway list-virtual-machines --query 'VirtualMachines' --output json)

# Check if all_vms is empty
if [ "$all_vms" == "[]" ]; then
    echo "No virtual machines found."
    exit 0
fi

# Initialize identified issues array
identified_issues=()

# Function to process each VM
process_vm() {
    local resource_arn=$1
    local resource_name=$2

    # Get the tags of the virtual machine using the Resource Groups Tagging API
    tags=$(aws resourcegroupstaggingapi get-resources --resource-arn-list "$resource_arn" --query 'ResourceTagMappingList[0].Tags' --output json 2>/dev/null)
    if [ $? -ne 0 ]; then
        echo "Failed to retrieve tags for resource ARN: $resource_arn"
        tags="{}"
    fi

    # # Debug statement to print tags before processing with jq
    # echo "Tags before jq: $tags"

    # Convert tags to a single-line JSON string
    tags=$(echo "$tags" | jq -c '.')

    # # Debug statement to print tags after processing with jq
    # echo "Tags after jq: $tags"

    # Get the last backup date
    last_backup=$(aws backup list-backup-jobs --by-resource-arn "$resource_arn" --query 'BackupJobs[?State==`COMPLETED`]|[0].CompletionDate' --output text | sort -r | head -n 1)

    # Convert last_backup to the same format as current_date
    if [ "$last_backup" != "None" ]; then
        last_backup=$(date -j -f "%Y-%m-%dT%H:%M:%S" "$(echo "$last_backup" | cut -d. -f1)" +"%Y-%m-%d")
    fi

    # Print the VM name, tags, and last backup date on one line
    echo "VM Name: $resource_name, Tags: $tags, Last Backup Date: $last_backup"

    # Get the path from the tags
    path=$(echo "$tags" | jq -r '.[] | select(.Key == "aws:backup-gateway:path") | .Value')

    if [[ "$path" == /1155/vm/Production* ]] && ([[ "$last_backup" == "None" ]] || [[ "$last_backup" != "$current_date" ]]); then
        identified_issues+=("VM Name: $resource_name, Tags: $tags, Last Backup Date: $last_backup")
    fi
}

# Read all VMs into an array
IFS=$'\n' read -r -d '' -a vms < <(echo "$all_vms" | jq -c '.[]' && printf '\0')

# Iterate over each virtual machine using a for loop
for vm in "${vms[@]}"; do
    # Debug statement to print each VM
    # echo "Processing VM: $vm"

    # Check if the VM entry is a valid JSON object
    if ! echo "$vm" | jq empty; then
        echo "Skipping invalid VM entry: $vm"
        continue
    fi

    resource_arn=$(echo "$vm" | jq -r '.ResourceArn')
    resource_name=$(echo "$vm" | jq -r '.Name')

    # Check if resource_arn and resource_name are not empty
    if [[ -z "$resource_arn" || -z "$resource_name" ]]; then
        echo "Skipping VM with missing ResourceArn or Name: $vm"
        continue
    fi

    process_vm "$resource_arn" "$resource_name"
done


# Debugging the identified_issues array
echo "Identified issues array contents:"
for issue in "${identified_issues[@]}"; do
    echo "$issue"
done

# Print identified issues
if [ ${#identified_issues[@]} -ne 0 ]; then
    echo "IDENTIFIED ISSUES:"
    for issue in "${identified_issues[@]}"; do
        echo "$issue"
    done
else
    echo "All VMs in production backup gateway paths have current backups."
fi

# Exit with a success status
exit 0