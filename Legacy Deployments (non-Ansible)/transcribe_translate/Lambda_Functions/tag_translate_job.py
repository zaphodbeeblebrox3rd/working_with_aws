import boto3
import json

# Apologies, I needed to hard-code the account ID but the code is mostly portable otherwise.
account_id = '<enter account id>'

def lambda_handler(event, context):
    # Parse the EventBridge event
    detail = event['detail']

    translate_job_name = detail['TranslationJobName']

    # Create a Translate client
    translate = boto3.client('translate')

    # Use the TranslationJobName to look up the Translate job
    response = translate.get_translation_job(TranslationJobName=translate_job_name)
    print(response)
    translate_job = response['TranslationJob']
    
    # For troubleshooting, display the entire translate job in the CloudWatch logs
    print(translate_job)
    
    # Get the bucket URI from the translate job    
    bucket_uri = translate_job['TranslationFileUri']
    print(bucket_uri)

    # Get the bucket name from the bucket URI
    bucket_name = bucket_uri.split('/')[3]
    print(bucket_name)

    # Pull the region from the bucket_uri
    region = bucket_uri.split('.')[1]
    print(region)


    # Tag the Translate job
    translate.tag_resource(
        ResourceArn=f"arn:aws:translate:{region}:{account_id}:translation-job/{translate_job_name}",
        Tags=[
            {
                'Key': 'Owner',
                'Value': bucket_name
            }
        ]
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Translate job tagged successfully')
    }
