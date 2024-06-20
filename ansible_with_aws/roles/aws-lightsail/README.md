qqq# AWS-Lightsail
The role will spin up a new Lightsail instance in AWS.  

## Requirements
You need an AWS account.  At the logon creen, instead of the Management Console click on Command Line or Programmatic Access.  Use the block for Set AWS environment variables prior to execution of the playbook.

THIS WILL NOT WORK UNLESS YOU SET YOUR AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, AND AWS SESSION TOKEN AS PER THE STEP ABOVE!  Also, note that these credentials expire after 30 minutes.

## Host, Group, or Role Variables
**ALL VARIABLES FOR THE LIGHTSAIL INSTANCE ARE ASSIGNED IN THIS FILE: site-playbooks/vars/aws_lightsail.yaml** 

There are no Host variables being used.  This is because the Host is actually localhost.  This means you will not be touching anything in the usual files where you would add vars for one of our on-premise VMs:
 - inventory/host_vars/ **LEAVE IT ALONE**
 - inventory/group/vars/ **LEAVE IT ALONE**
 - inventory/hosts/ **LEAVE IT ALONE**
 - /etc/hosts **LEAVE IT ALONE**

The aws_instance_name variable is the only one that is strictly required.  All other variables will fall back on the defaults unless otherwise specified.  The example aws_lightsail.yaml file below shows one instance that is defined only by name.  This means you could simply add a named instance to this file, run the playbook, and the result will be a functional webserver.

### Example site_playbooks/vars/aws_lightsail.yaml
```
---
lightsail_instance:
  - aws_instance_name: <instance_name>
    aws_region: <region>
    aws_availability_zone: <availability_zone>
    lightsail_snapshot_name: <snapshot_name>
    aws_key_pair_name: <key_pair_name>
    aws_owner: <owner>
    aws_bundle_id: nano_2_0
    aws_blueprint_id: lamp_8_bitnami
    aws_http_allowed_networks: 0.0.0.0/0
    aws_https_allowed_networks: 0.0.0.0/0
    aws_ssh_allowed_networks:
      - <ssh_allowed_network1>
      - <ssh_allowed_network2>
      - <ssh_allowed_network3>
    aws_user_data: echo
  - aws_instance_name: <instance_name>
    aws_region: <region>
    aws_availability_zone: <availability_zone>
    lightsail_snapshot_name: <snapshot_name>
    aws_key_pair_name: <key_pair_name>
    aws_owner: <owner>
    aws_bundle_id: nano_2_0
    aws_blueprint_id: lamp_8_bitnami
    aws_http_allowed_networks: 0.0.0.0/0
    aws_https_allowed_networks: 0.0.0.0/0
    aws_ssh_allowed_networks:
      - <ssh_allowed_network1>
      - <ssh_allowed_network2>
      - <ssh_allowed_network3>
    aws_user_data: echo
  - aws_instance_name: minimal-config
    aws_user_data: echo
```

### group_vars
As mentioned above, you should not need to edit group vars.  The defaults are all defined here, but they should not be changed.  However, there is a var worth mentioning.  aws_user_data allows feeding a short bash script into the aws cli.  This is being used to activate Crowdstrike Falcon antivirus and to set the MOTD.
```
aws_user_data: |
  #!/bin/bash
  apt-get install /home/bitnami/<package.deb> -y
  sleep 30
  systemctl start <service>
  systemctl enable <service>
  cat << EOF > /etc/motd.new


  This computer system is owned by <company name> and is for
  authorized use only.  Individuals using this computer system are subject
  to having all of their activities on this system monitored and recorded
  by system personnel.  Anyone using this system expressly consents to
  such monitoring and is advised that if such monitoring reveals possible
  criminal activity or policy violation, system personnel may provide the
  evidence of such monitoring to law enforcement or other officials.

  EOF
  cat /etc/motd >> /etc/motd.new
  mv /etc/motd.new /etc/motd
```
Note: aws_user_data will allow the feeding of any bash or python script into the startup of a Lightsail instance.  It is not encouraged, but this could possibly used to replace the standard setup script with something customized to a particular instance.  In the site_playbooks/vars/aws_lightsail.yaml example above, you will see that aws_user_data is set to 'echo'.  This overrides the setup script, allowing me to demonstrate the creation of lightsail instances without clouding up the Crowdstrike Falcon console with a giant list of phantom machines.

## Finding valid values for variables
Use aws cli to get a list of values you could use instead of 'nano_2_0' for the aws_bundle_id.  If you need a greater amount of CPU or memory resources than the default, you will be using this variable.  NOTE: Deviate from the default with caution.  Non-default settings may be expensive.
```
aws lightsail get-bundles
```

The aws_blueprint_id is a machine image.  This includes the OS and the software stack.  If you are spinning up a webserver, leave it at the default lamp_8_bitnami.  The list of blueprints is growing.  At the time of writing this README, there are research stacks in the works that should be distributed to the US regions soon.  You may need to pipe the output into grep to find what you are looking for.
```
aws lightsail get-blueprints
```

aws_region and aws_availability zone are related.  If you are changing these from the defaults, take care that they do not conflict with each other.  For example, setting the region to us-east-2 and then the AZ to us-east-1a would not make sense and it would cause a problem.
```
aws lightsail get-regions
aws ec2 describe-availability-zones --region <your region>
```

## Usage
Run the command multiple times if you need to.  The playbook is idempotent; it will not break a Lightsail instance that already exists.  The worst thing that could happen is that the owner tag or firewall could get changed so that it matches the specs in site_playbooks/vars/aws_lightsail.yaml

All variables are defined in site_playbooks/vars/aws_lightsail.yaml, so nothing special needs to be passed into the playbook run:
``` 
ansible-playbook site-playbooks/aws-lightsail.yml 
```

## SSL Cert
The painful process of generating a CSR, submitting to InCommon, waiting a day or two, receiving a cert with an old sha-1 signed Trusted Root CA, and fumbling around with the certificate chain to get the server to accept it is obsolete now.

That said, the process is not fully automated.  The reason for this is the dependence of this process on a valid DNS record linked to the public IP address of the instance, which you will not know until the playbook runs to completion.

First, sort the Elastic IP assignment and external DNS records.  Give the DNS records at least a few minutes to replicate.  Then connect to the Lightsail instance run the following script, and follow the prompts:
```
sudo /opt/bitnami/bncert-tool
```

When complete, the valid SSL cert will be immediately applied and all SSL cert renewals will happen automatically going forward.

## FAQ
### Why can't I specify a blueprint_id for a different OS and software stack?
* The role currently depends on a snapshot for some of the required security config.  As the aws cli and the community.aws.lightsail ansible module continue to be developed, this role will be made more flexible.

### Why am I getting errors regarding the security token being expired?
* It is likely that you forgot to enter your AWS credentials, or that they expired.  They are only valid for 30 minutes.  Get fresh credentials from the https://uchicago.awsapps.com/start#/ page.  When you click on "Command line or programmatic access" you will see a block of commands under "Option 1: Set AWS environment variables (Short-term credentials)" which you can copy & paste into the terminal. 

### Why isn't ansible able to connect to the instance for further configuration?
* Lightsail instances are designed to be lightweight.  They are preconfigured, and they don't have the same functionality as most full OS instances.  For example, usermod/useradd is not an available command, so no 'ansible' account can be created.

### What is the point of doing anything in Lightsail?  Why not EC2 instances for everything?
* There are a lot of reasons:
    - Lightsail instances cost $3.50 per month, whereas a similar EC2 instance would be about $30.  The elastic IP address actually costs more than running the Lightsail instance!  This allows you to create a DEV and PRD server for every deployment, and to offer this service to researchers fully subsidized by SSD.
    - Deployment speed.  You can spin up a Lightsail instance in less than a minute.
    - Performance.  Lightsail provides a very streamlined, curated image which is tested extensively to perform well with minimal resources.
    - Reduced surface area.  There are no extraneous unnecessary services, so there are fewer vulnerabilities.
    - Certificate management.  A SSL certificate can be requested and installed in less than a minute, and it auto-renews without any need for action on your part.

## Dependencies
------------
- Ansible 2.5 or later
- Python 3.6+

## Author Information
------------------
Eric Hoy <hoy@uchicago.edu>
