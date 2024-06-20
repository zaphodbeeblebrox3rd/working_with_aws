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


## Support

You are on your own.  No support is provided.