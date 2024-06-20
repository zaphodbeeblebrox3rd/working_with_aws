# AWS IAM Policy Role

This Ansible role is designed to create and manage AWS IAM policies. It automates the process of creating IAM groups, attaching policies to these groups, and ensuring that your AWS environment adheres to defined access and security standards.

Note that this role needs to be used carefully in a multi-account environment.  When you have separate AWS accounts, you need to ensure that the IAM Policy is created in the correct account. The only logical way to do this is to specify the account ID inside a site playbook, and leverage string matching on the name of the IAM Policy.  See the Example Playbook section below for an example of how to use the `aws_account_id` variable to specify the account ID.

## Requirements

- **Ansible**: This role requires Ansible 2.9 or newer.
- **AWS Account**: You must have an AWS account and sufficient permissions to create and manage IAM policies and groups.
- **AWS CLI**: The AWS Command Line Interface must be installed and configured on the machine executing the playbook.
- **Python**: Python 3.6 or newer is required, along with the `boto3` and `botocore` libraries for interacting with AWS services.

## Role Variables

The role automatically extracts all necessary variables with no need to define them. Here are the key variables:

- `policy_file.path`: The path to the JSON file containing the IAM policy definition.
- `iam_group_name`: The name of the IAM group to which the policy will be attached. If not specified, the role will derive a name based on the policy file name.

The important thing is that you must have a JSON file in the `site-playbooks/aws-iam-policies` directory. The role will not work if the file is not present, and the naming of the file must be `policy_name.json`.

## Dependencies

This role depends on the `amazon.aws` collection. Ensure you have the latest version installed using the following command:

```
bash
ansible-galaxy collection install amazon.aws
```

## Example Playbook

Below is an example playbook that demonstrates how to use the `aws-iam-policy` role to create IAM policies related to S3 in AWS account # 123456789.

```yaml
---
- hosts: localhost
  gather_facts: no
  vars_files:
    - vars/aws_credentials.yml
  vars:
    - aws_account_id: 123456789
  tasks:
    - name: Find IAM policy JSON files
      ansible.builtin.find:
        paths: aws-iam-policies
        patterns: '*S3.json'
      register: json_files

    - name: Deploy each IAM policy
      include_role:
        name: aws-iam-policy
      loop: "{{ json_files.files }}"
      loop_control:
        loop_var: policy_file
```

This example site-playbook will create policies related to Transcribe/Translate to AWS account# 234567890:

```yaml
---
- name: Deploy Transcription/Translation IAM policies
  hosts: localhost
  gather_facts: no
  vars_files:
    - vars/aws_credentials.yml
  vars:
    - aws_account_id: 234567890
  tasks:
    - name: Find IAM policy JSON files
      ansible.builtin.find:
        paths: aws-iam-policies
        patterns: 'Transcription*'
      register: json_files
```

## Author Information
------------------
Eric Hoy <hoy@uchicago.edu>.  If you have any issues, feel free to fix them. 
