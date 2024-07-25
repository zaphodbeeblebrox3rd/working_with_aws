#!/bin/bash
# Show all transcribe jobs on an account and their tags
# Author: Eric Hoy
# Date: 2024-06-24

#Define variables
REGION="<region>"
ACCOUNT_ID="<account_id"
DEFAULT_OWNER_TAG="<default_owner_tag>" #if no owner tag is found, this value will prevent issues from being empty.

# Initialize next_token
next_token=""

# Loop to handle pagination
while true; do
    # Fetch a page of transcription jobs
    if [ -z "$next_token" ]; then
        result=$(aws transcribe list-transcription-jobs --region $REGION)
    else
        result=$(aws transcribe list-transcription-jobs --region $REGION --next-token $next_token)
    fi

    # Extract job names and next token
    jobs=$(echo "$result" | jq -r '.TranscriptionJobSummaries[].TranscriptionJobName')
    next_token=$(echo "$result" | jq -r '.NextToken // empty')

    # Loop through each job to fetch tags
    for job in $jobs; do
        # Construct the ARN for the job
        arn="arn:aws:transcribe:$REGION:$ACCOUNT_ID:transcription-job/$job"
        # Get tags and extract the Owner tag
        owner_tag=$(aws transcribe list-tags-for-resource --resource-arn "$arn" --region $REGION | jq -r '.Tags[] | select(.Key == "Owner").Value')
        # if [ -z "$owner_tag" ]; then
            # owner_tag=$DEFAULT_OWNER_TAG
            # Set the empty owner tag to the default
            # aws transcribe tag-resource --resource-arn "$arn" --tags Key=Owner,Value="$owner_tag" --region $REGION
        # fi
        creation_time=$(aws transcribe get-transcription-job --transcription-job-name "$job" --region $REGION | jq -r '.TranscriptionJob.CreationTime')
        echo "Job Name: $job, Creation Time: $creation_time, Owner Tag: $owner_tag"
    done

    # Break the loop if there is no next token
    if [ -z "$next_token" ]; then
        break
    fi
done
