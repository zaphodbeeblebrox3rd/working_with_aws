# S3, Transcribe, and Translate Handling with Multiple Projects on a Single AWS Account

## Overview
I had the opportunity to work on a case where a single AWS account was designated to be used for transcription and translation of audio files by multiple different users and projects.  There were two main challenges:
1. Separating out access so that users could not see each other's work.  Data for each research project needed to be restricted to that project team.
2. Showback billing.  I needed to set this up in a way that Cost Explorer could be utilized for easily attributing costs on a per-project basis.

In summary, there are two important elements.  Firstly, access to S3 and other services needed to be clearly defined by the SSO-linked IAM role assigned to users on each project team.  Secondly, resource tagging needed to be enabled in a way that we could confidently report on costs without depending on the users to tag their jobs in a certain way.

IAM policies needed to be defined for each project team to ensure that each team could only see their own data.  Then, EventBridge was utilized to trigger a Lambda function for tagging each job with an Owner tag that my organization uses for showback billing. 

## Important Note
Resource Tagging is not currently a property of Translate Jobs.  I think it is quite reasonable to allow this and I am clueless as to why this is.  https://docs.aws.amazon.com/translate/latest/APIReference/API_TextTranslationJobProperties.html

## Prerequisites

- AWS account with admin access to the account for setting up S3 buckets and IAM policies.


## Configuration for Transcribe and Translate

### Transcribe
1. Create the S3 buckets first. One bucket for each project team.
2. Set up IAM policies for each bucket, according to the Transcribe-Users-Project1 example.  The bucket name goes into each policy.  Attach those IAM policies to their corresponding IAM role for each project team.
3. Create a IAM policy for the lambda function based on the Lambda-Resource-Tag example.  Insert your AWS Account ID into the function.  Create an IAM role and attach this new policy.  
3. Create the Lambda function for tagging Transcribe resources.  Use the tag_transcribe_job.py file as a guide.  Attach the IAM role from the previous step.
4. Set up EventBridge to trigger the Lambda function on transcription job completion events.  Use the transcribe_event_pattern.json file as a guide.  NOTE: this also requires specifying the account ID in the event pattern. 

### Translate - NOT YET SUPPORTED BY AWS
1. Assuming that you have already set up your IAM roles and policies for Transcribe, you will theoretically use the S3 buckets and IAM policies you already created.
2. Create the Lambda function for tagging Translate resources.  Use the tag_translate_job.py file as a guide.  Use the same IAM role you attached to the Transcribe Lambda function. Don't forget to insert your own AWS Account ID into the Lambda function code.
3. Set up EventBridge to trigger the Lambda function on translation job completion events.  Use the translate_event_pattern.json file as a guide.  NOTE: this also requires specifying the account ID in the event pattern. 


### Cloudwatch  

Create a Cloudwatch log group for each Lambda function:
1. Go to the CloudWatch Logs service in the AWS Management Console
2. Click on "Log groups" in the left navigation pane
3. Click on "Create log group" button
4. Enter "/aws/lambda/tag<service_name>Job" as the log group name
5. Click "Create log group" to create the missing log group
6. Go back to the Lambda function configuration page
7. Click on the "Monitoring tools" tab
8. Under "Log group", select the newly created log group
9. Click "Save" to update the Lambda function configuration


## Usage

Once deployed, the Lambda function will automatically be triggered by EventBridge upon the completion of transcription jobs. It will:

- Retrieve the transcription job details.
- Extract the S3 bucket URI from the transcription job.
- Parse the bucket name and AWS region from the URI.
- Tag the transcription job with the bucket name under the tag key Owner.

This works because users on project teams will be restricted from creating service-managed S3 buckets.  This means the Transcribe and Translate jobs for a project team will not be visible to the other project teams.


## Logging

The function logs various details about the transcription job to CloudWatch, which can be used for debugging and monitoring the Lambda function's operations.


## Limitations

The function assumes the S3 bucket URI is in a specific format to correctly parse the bucket name and region. Changes in URI format may require updates to the parsing logic.  Also, the tags will be determined based on the bucket name.  This means the actual username is not stored in the tag.  In other words, you must ensure that each user/project needing to be separated out in Cost Explorer will have its own bucket with a meaningful name that ties it back to its project team.


## Support
I'm not available for support, but I would appreciate any feedback you have.
This README provides a basic guide to deploying and understanding the function. Ensure all configurations and permissions are correctly set according to your AWS environment and security guidelines.