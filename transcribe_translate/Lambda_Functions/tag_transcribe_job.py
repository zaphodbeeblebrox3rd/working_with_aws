import boto3
import json

# Apologies, I needed to hard-code the account ID but the code is mostly portable otherwise.
account_id = '<enter account id>'

def lambda_handler(event, context):
    # Parse the EventBridge event
    detail = event['detail']

    transcribe_job_name = detail['TranscriptionJobName']

    # Create a Transcribe client
    transcribe = boto3.client('transcribe')

    # Use the TranscriptionJobName to look up the Transcribe job
    response = transcribe.get_transcription_job(TranscriptionJobName=transcribe_job_name)
    print(response)
    transcribe_job = response['TranscriptionJob']
    
    # For troubleshooting, display the entire transcribe job in the CloudWatch logs
    print(transcribe_job)
    
    # Get the bucket URI from the transcribe job    
    bucket_uri = transcribe_job['Transcript']['TranscriptFileUri']
    print(bucket_uri)

    # Get the bucket name from the bucket URI
    bucket_name = bucket_uri.split('/')[3]
    print(bucket_name)

    # Pull the region from the bucket_uri
    region = bucket_uri.split('.')[1]
    print(region)


    # Tag the Transcribe job
    transcribe.tag_resource(
        ResourceArn=f"arn:aws:transcribe:{region}:{account_id}:transcription-job/{transcribe_job_name}",
        Tags=[
            {
                'Key': 'Owner',
                'Value': bucket_name
            }
        ]
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Transcribe job tagged successfully')
    }
