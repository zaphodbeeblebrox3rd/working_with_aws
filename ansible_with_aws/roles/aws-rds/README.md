# AWS-RDS
The role will spin up a new Aurora RDS Cluster instance in AWS.  

## Requirements
You need an AWS account.  At the logon creen, instead of the Management Console click on Command Line or Programmatic Access.  Use the block for Set AWS environment variables prior to execution of the playbook.

THIS WILL NOT WORK UNLESS YOU SET YOUR AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, AND AWS SESSION TOKEN AS PER THE STEP ABOVE!  Also, note that these credentials expire after 30 minutes.

## Host, Group, or Role Variables
**ALL VARIABLES FOR THE RDS INSTANCES ARE ASSIGNED IN THIS FILE: site-playbooks/vars/aws_rds.yaml** 

There are no Host variables being used.  This is because the Host is actually localhost.  This means you will not be touching anything in the usual files where you would add vars for one of our on-premise VMs:
 - inventory/host_vars/ **LEAVE IT ALONE**
 - inventory/group/vars/ **LEAVE IT ALONE**
 - inventory/hosts/ **LEAVE IT ALONE**
 - /etc/hosts **LEAVE IT ALONE**


### Example site_playbooks/vars/aws_rds.yaml
```
---
rds_instance:
  - aws_rds_cluster_identifier: <cluster_identifier>
    aws_region: <region>
    aws_availability_zone: <availability_zone>
    aws_owner: <owner>
    aws_copy_tags_to_snapshot: <copy_tags_to_snapshot>
    aws_rds_engine: <engine>
    aws_rds_engine_mode: serverless
    aws_rds_engine_version: 15.2
    aws_rds_auto_minor_version_upgrade: yes
    aws_rds_cluster_storage: Aurora I/O Optimized
    aws_rds_port: 5432
    aws_rds_master_username: postgres
    aws_rds_master_user_password: <master_user_password>
    aws_rds_database_name: <database_name>
    aws_vpc_security_group: <vpc_security_group>
    aws_rds_backup_retention_period: 10
    aws_rds_storage_encrypted: yes
    aws_rds_kms_key_id: <kms_key_id>
    aws_rds_scaling_auto_pause: True
    aws_rds_max_capacity: 16
    aws_rds_min_capacity: 2
```

## Usage
Run the command multiple times if you need to.  The playbook is idempotent; it will not break an RDS instance that already exists. 

All variables are defined in site_playbooks/vars/aws_rds.yaml, so nothing special needs to be passed into the playbook run:
``` 
ansible-playbook site-playbooks/aws-rds.yml 
```

## Database Cert
Authentication to the database can be done via certificate.  The instructions on how to manage this need to be added to this section.  


## FAQ

### Why am I getting errors regarding the security token being expired?
* It is likely that you forgot to enter your AWS credentials, or that they expired.  They are only valid for 30 minutes.  Get fresh credentials from the https://uchicago.awsapps.com/start#/ page.  When you click on "Command line or programmatic access" you will see a block of commands under "Option 1: Set AWS environment variables (Short-term credentials)" which you can copy & paste into the terminal.

### Why isn't ansible able to connect to the instance for further configuration?
* RDS server instances are designed so that there is no underlying EC2 instance to be managed.  AWS handles the underlying machines running the cluster, so the Operating System is a "black box" configuration.

### What is the point of doing anything in RDS?  Why not EC2 instances for everything?
* There are a lot of reasons:
    - A database cluster built in EC2 would need the clustering configuration to be performed, and an elastic load balancer.  The number of EC2 instances could become high.
    - Patch management of the EC2 instances would become burdensome.
    - Deployment speed.  A complex configuration is more manageable and does not require a software engineer to develop.
    - Performance.  Aurora "Serverless" RDS clusters are auto-scalable for CPU/Memory/Storage resources. They are able to grow without blowing up.
    - Reduced surface area.  There are no extraneous unnecessary services, so there are fewer vulnerabilities.

## Dependencies
------------
- Ansible 2.7 or later
- Python 3.6+

## License
-------
This is private to the University of Chicago.


## Author Information
------------------
Eric Hoy <hoy@uchicago.edu>
