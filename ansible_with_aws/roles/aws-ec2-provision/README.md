# AWS-EC2-GPU
The role will spin up a new EC2 instance with specified host type. The configuration will be performed by the aws-ec2-configure role, which will also be launched by the aws-ec2.yml site playbook. It is under construction

## Requirements
You need to define an AWS account in the site-playbook launching this role, and the credentials need to be included in the site-playbook vars/aws_credentials.yml

## Host, Group, or Role Variables
Variables are tricky with EC2.  Pay close attention to this section!

With this pair of roles, there are variables that need to be set in multiple config filess:
1. inventory/host_vars can optionally have a file to override any group vars in place.  It will be relatively lightweight.  These affect the Operating System and configuration within the EC2 instance
2. site-playbooks/vars/aws_ec2.yaml is NOT optional.  There are no default values to fall back on.  This means that ALL vars need to be populated per the example below.
3. If you're not using an existing security group already defined in site-playbooks/vars/aws_security_groups.yaml, you need to define the new security group in this file.

ec2_instance:
  - aws_instance_name: <instance_name>
    aws_region: <region>
    aws_availability_zone: <availability_zone>
    aws_key_pair_name: <key_pair_name>
    aws_owner: <owner>
    aws_instance_type: <instance_type>
    aws_security_group: <security_group>
    aws_subnet: <subnet>
    aws_ami_id: <ami_id>
    aws_vpc_subnet_id: <vpc_subnet_id>
    aws_elastic_ip: <elastic_ip>
    aws_public_ip: <public_ip>

Use the existing config as a guideline on how to specify the ssh key pair, instance type (defines CPU and memory), AMI (operating system base image), and security group (firewall)

Note that the host-based firewall will not be configured so that the security group will be the source of truth on the firewall configuration

## Example site-playbook
Each AWS account needs its own site-playbook to loop through the security groups file for the relevant AWS account in site-playbooks/vars.  It then loops through the ec2_instance list defined in the site-playbook/vars/aws_ec2.yaml, and provision the EC2 instance.  It will authenticate to the AWS account based on the corresponding IAM user credentials in aws_credentials.yml.  The site-playbook aws-ec2-security-groups.yml will create the security groups for the EC2 instances.  The site-playbook aws-ec2-provision.yml will provision the EC2 instances.
```yaml
---
- name: Create AWS Security Groups
  hosts: localhost
  gather_facts: no
  vars_files:
    - vars/aws_security_groups_<account#>.yaml
    - vars/aws_credentials.yml
  vars:
    aws_account_id: <account_id>
  tasks:
    - name: Set AWS credentials and region for session
      set_fact:
        aws_access_key: "{{ aws_accounts[aws_account_id]['aws_access_key_id'] }}"
        aws_secret_key: "{{ aws_accounts[aws_account_id]['aws_secret_access_key'] }}"
        aws_region: "{{ aws_accounts[aws_account_id]['region'] }}"

    - name: Configure AWS credentials
      shell: |
        aws configure set aws_access_key_id "{{ aws_access_key }}" &&
        aws configure set aws_secret_access_key "{{ aws_secret_key }}" &&
        aws configure set default.region "{{ aws_region }}"

    - name: Create security group
      amazon.aws.ec2_group:
        name: "{{ item.security_group_name }}"
        description: "{{ item.security_group_name }}"
        vpc_id: "{{ item.vpc_id }}"
        region: "{{ item.region }}"
        rules: "{{ item.rules }}"
        rules_egress: "{{ item.rules_egress }}"
      loop: "{{ aws_security_groups }}"
      
- hosts: localhost
  gather_facts: no
  vars_files:
    - vars/aws_ec2.yaml
  tasks:
    - name: loop through role for each ec2 inventory item in the dictionary
      include_role:
        name: aws-ec2-provision
      loop: "{{ ec2_instance }}"
```

## Example Run

This basic example is the only one that should be referenced at this time:
```
sudo ansible-playbook /etc/ansible/site-playbooks/aws-ec2-<account #>.yml
```

If you need to limit the config to a target server not yet provisioned in AWS, add localhost. localhost is the ansible controller itself, and only needed to interact with AWS for the provisioning of the EC2 instance.  It will be automatically omitted from the aws-ec2-configure role
```
sudo ansible-playbook /etc/ansible/site-playbooks/aws-ec2-account-<account #>.yml --limit <target_server>,localhost
```

It is preferable to run the play without specifying any limits.  These roles were written with particular attention to idempotency in order to accommodate running the play this way.
```
sudo ansible-playbook /etc/ansible/site-playbooks/aws-ec2.yml
```

If this is confusing, or if you are uncertain how the play will behave for whatever reason, perform a dry run
```
sudo ansible-playbook /etc/ansible/site-playbooks/aws-ec2.yml --dry-run
```

Dependencies
------------
- Ansible 2.7 or later
- Python 3.11+


Author Information
------------------

Eric Hoy <hoy@uchicago.edu>
