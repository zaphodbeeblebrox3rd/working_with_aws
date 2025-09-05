# Ansible with AWS

This repository contains Ansible roles for provisioning and configuring a variety of AWS resources. Working with AWS using Ansible can be complex, so this repository provides a structured approach to managing AWS infrastructure as code.

## Overview

The `ansible_with_aws` codebase provides five comprehensive Ansible roles for managing various AWS services:

- **aws-iam-policy**: Create and manage AWS IAM policies
- **aws-ec2-provision**: Provision and configure EC2 instances
- **aws-cloudformation-deploy**: Deploy resources using AWS CloudFormation templates
- **aws-lightsail**: Manage AWS Lightsail instances
- **aws-rds**: Provision and configure RDS database instances

## Prerequisites

### Python Environment Setup

1. **Python 3.11 or later** (recommended)
2. **Virtual Environment** (recommended):
   ```bash
   python3 -m venv ansible-aws-env
   source ansible-aws-env/bin/activate  # On Windows: ansible-aws-env\Scripts\activate
   ```

3. **Install Required Python Packages**:
   ```bash
   pip install ansible boto3 botocore
   ```

### AWS Account Setup

1. **AWS CLI Installation**:
   ```bash
   # macOS
   brew install awscli
   
   # Or using pip
   pip install awscli
   ```

2. **AWS Credentials Configuration**:
   ```bash
   aws configure
   ```
   Provide your:
   - AWS Access Key ID
   - AWS Secret Access Key
   - Default region name
   - Default output format (json recommended)

3. **IAM User Requirements**:
   - Create an IAM user with appropriate permissions for the services you plan to manage
   - Attach policies that grant necessary permissions for EC2, IAM, CloudFormation, Lightsail, and RDS operations
   - Ensure the user has programmatic access enabled

4. **AWS Account Number**:
   - Note your AWS account number (found in the AWS Management Console top-right corner)
   - This will be used in playbook variable files

## Ansible Roles

### aws-iam-policy
Manages AWS IAM policies and policy attachments. This role can:
- Create custom IAM policies from JSON templates
- Attach policies to users, groups, or roles
- Validate AWS credentials before operations

### aws-ec2-provision
Provisions and configures EC2 instances with:
- Custom instance types and AMI selection
- Security group configuration
- Key pair management
- Tagging and metadata setup

### aws-cloudformation-deploy
Deploys AWS resources using CloudFormation templates:
- Stack creation and updates
- Parameter management
- Stack status monitoring
- Rollback capabilities

### aws-lightsail
Manages AWS Lightsail instances including:
- Instance creation and configuration
- Networking setup (VPC, subnets, security groups)
- Instance state management
- Resource tagging

### aws-rds
Provisions and manages RDS database instances:
- Database engine selection (MySQL, PostgreSQL, etc.)
- Instance sizing and configuration
- Security group and subnet group setup
- Backup and maintenance window configuration

## Usage

### Running Playbooks

1. **Navigate to the site-playbooks directory**:
   ```bash
   cd site-playbooks
   ```

2. **Configure Variables**:
   - Copy and modify the appropriate variable files in the `vars/` directory
   - Update account-specific variables (replace `<account#>` with your account number)
   - Configure AWS credentials in `vars/aws_credentials.yml`

3. **Run a Playbook**:
   ```bash
   ansible-playbook -i inventory <playbook-name>.yml
   ```

### Example Playbook Execution

```bash
# Deploy IAM policies
ansible-playbook -i inventory aws-iam-deploy-s3-policy-123456789.yml

# Provision EC2 instances
ansible-playbook -i inventory aws-ec2-account-123456789.yml

# Deploy CloudFormation stack
ansible-playbook -i inventory aws-cloudformation-wrapper.yml
```

### Variable Configuration

Each playbook uses variables defined in the `vars/` directory:
- `aws_credentials.yml`: AWS authentication settings
- `aws_ec2_<account#>.yaml`: EC2-specific configuration
- `aws_lightsail_<account#>.yaml`: Lightsail configuration
- `aws_rds.yaml`: RDS database settings
- `aws_security_groups_<account#>.yaml`: Security group definitions

## Directory Structure

```
ansible_with_aws/
├── roles/                    # Ansible roles
│   ├── aws-iam-policy/      # IAM policy management
│   ├── aws-ec2-provision/   # EC2 instance provisioning
│   ├── aws-cloudformation-deploy/  # CloudFormation deployments
│   ├── aws-lightsail/       # Lightsail management
│   └── aws-rds/            # RDS database management
├── site-playbooks/         # Main playbooks
│   ├── vars/               # Variable files
│   ├── aws-iam-policies/   # IAM policy JSON templates
│   └── files/              # Additional files
└── inventory/              # Ansible inventory files
```

## Support

This repository is provided as-is for educational and reference purposes. No formal support is provided.