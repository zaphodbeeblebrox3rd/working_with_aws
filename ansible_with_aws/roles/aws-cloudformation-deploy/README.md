# aws-cloudformation-deploy 
A wrapper for AWS Cloudformation.  It is used to deploy Cloudformation templates.

## Requirements
You need an AWS account.  The account needs an IAM user with admin permissions.  Technically, the role will function even if the vars file is not encrypted BUT MAKE SURE YOU ENCRYPT THE FILE WITH ANSIBLE VAULT ANYWAY!  The key ID and secret need to be configured in the site-playbooks/vars/aws_credentials.yml in the following format:

>aws_accounts:
>  - aws_account_id: <account_id>
>    aws_access_key_id: <access_key_id>
>    aws_secret_access_key: <secret_access_key>
>    region: <region>

The Cloudformation template is the meat and potatoes that defines the stack.  This is where most of your work is going into. The template file should be stored in site-playbooks/files in yaml format.  Do not attempt to store the file under the role because the shell execution environment will be site-playbooks.

This role can be launched by a site playbook.  It will use the variables from the site-playbooks/vars/aws_credentials.yml file and it must have additional variables specified inside the playbook.  Here is an example for a stack that deploys a load balancer.

>---
>hosts: localhost
>gather_facts: no
>vars_files:
>  - vars/aws_credentials.yml
>vars:
>  - aws_account_id: 
>  - cloudformation_template_path: files/<cf_template_path>
>  - cloudformation_stack_name: <stack_name>
>  - cloudformation_parameters:
>      - ParameterKey: VPCId
>        ParameterValue: <vpc_id>
>      - ParameterKey: Subnets
>        ParameterValue: <subnet1>,<subnet2>
>roles: 
>  - aws-cloudformation-deploy



## Example Run
After creating the playbook, launch it with no additional parameters.  Do not use --limit or --tags. 

```
sudo ansible-playbook /etc/ansible/site-playbooks/aws-cloudformation-wrapper.yml
```



Dependencies
------------
- Ansible 2.7 or later
- Python 3.11+
- awscli
- jinja2


