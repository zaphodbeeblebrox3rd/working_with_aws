# Ansible with AWS

This repository contains Ansible roles for provisioning and configuring a variety of AWS resources.  Working in AWS using Ansible is not easy, so this repository is intended to help you get started.


## Overview

The ansible_with_aws codebase provides Ansible roles and playbooks for managing various AWS services. It includes examples and configurations for IAM policies, EC2 provisioning, CloudFormation deployments, and more.


## Prerequisites

- Ansible 2.9 or later
- Python 3.6 or later
- Boto3 library for Python
- AWS CLI installed
- AWS credentials


## Key Components

**IAM Policies**: Automate the creation and management of AWS IAM policies.

**EC2 Provisioning**: Configure and launch EC2 instances with specific settings.

**CloudFormation**: Deploy resources using AWS CloudFormation templates.

**Lightsail**: Manage AWS Lightsail instances.


## Configuration

Ensure your AWS credentials are set up correctly and accessible to Ansible. You may need to configure specific variables in the playbooks to match your AWS environment.



## Usage

Navigate to the site-playbooks directory to find playbooks for deploying specific AWS services. Modify the variables in the playbook as needed and run the playbook using the following command:

```
ansible-playbook <playbook-name>.yml
```

### Transcribe Low Risk Stack

This approach to transcription and translation was done with the following mantra: "Upload/Download".  Users can upload their media files and then download the output with no fussing over job configuration, and with very little access (S3 only) to the AWS Console.  

To deploy the Transcribe Low Risk Stack, you need to have the AWS account number for the account you want to deploy to.  You also need an IAM User in the AWS Account that the Ansible controller will use to deploy the stack.  You can find the AWS account number by going to the AWS Management Console and looking at the account ID in the top right corner.  

The stack allows you to assign all users to a single SSO-Linked IAM role, which is ideally linked to a group in your Identity Management System.  The IAM role is granted access to read and write to all S3 buckets in the account, and it depends on bucket policies to deny access to all but the lambda functions, the user, and optionally the IAM user for Ansible.  

Users will log into the AWS Console, launching an EventBridge trigger which targets a lambda function to provision an S3 bucket with a dynamically created bucket policy. On upload of a media file to the Audio_Files prefix in the S3 bucket, an S3 event is triggered which launches the lambda function that orchestrates the transcription job with output to the Transcription_Output prefix in the user's bucket. 

Another lambda function converts the json output to a Word document for an easily readable transcript.  The user can then download the document from their bucket.

The same goes for translation, which accepts plaintext input files in the Translation_Input prefix and outputs to the Translation_Output prefix in json and Word document formats.  

Additionally, the stack includes a lambda function which provides an easily readable log of AWS Console logins.

The lambda functions are mostly designed to be inexpensive and fast, with the intention of scaling to handle many users and many jobs.  The only expensive function is the conversion of json to Word document format.  The functions are designed to be fault-tolerant, with a retry strategy of 3 attempts with an exponential backoff.  The lambda function also includes a custom resource to tag the S3 bucket with the user's identifying info.  The same approach is applied to the Transcribe jobs to allow for cost-tracking by tag for the S3 and Transcribe costs.  Unfortunately AWS does not support this approach with Translate, so cost tracking Translate services is unattainable at this time.




## Support

You are on your own.  No support is provided.