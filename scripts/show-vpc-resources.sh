#! /usr/bin/env bash
# Search a VPC id in AWS and enumerate its resources
# Maybe helpful to figure out whether a VPC is used, and what resources it contains
# Author: Eric Hoy
# Date: 2023-07-21

# Validate the AWS credentials 
#aws sts get-session-token --profile default

echo "Don't forget to set your AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AND AWS_SESSION_TOKEN in your environment variables if you are using short-term credentials"

#Show all VPCs on the account.  One line for each item showing OwnerId, VpcID, and CidrBlock
echo "Listing all VPCs on the AWS account"
aws ec2 describe-vpcs --query 'Vpcs[*].[OwnerId, VpcId, CidrBlock]'
echo ______________________________________________________________

#Show all Security Groups on the account.  One line for each item showing GroupId, GroupName, and VpcId
echo "Listing all Security Groups on the AWS account"
aws ec2 describe-security-groups --query 'SecurityGroups[*].[GroupId, GroupName, VpcId]'
echo ______________________________________________________________


read -p "Enter the VPC ID for more detail on that VPC " vpc_id
echo "Searching $vpc_id..."

# By listing all network interfaces, produce a reliable output of all instances
aws ec2 describe-network-interfaces --filters Name=vpc-id,Values=$vpc_id --query  'NetworkInterfaces[*].[AvailabilityZone, OwnerId, Attachment.InstanceId, PrivateIpAddresses[*].Association.PublicIp]'
aws ec2 describe-network-interfaces --filters Name=vpc-id,Values=$vpc_id --query  'NetworkInterfaces[*].[RequesterId,Description]'
echo ______________________________________________________________

# Show all Security Groups in the VPC
echo "Listing all security Groups inside VPC $vpc_id"
aws ec2 describe-security-groups --filters Name=vpc-id,Values=$vpc_id --query 'SecurityGroups[*].[GroupId, GroupName, VpcId]'
echo ______________________________________________________________

# Show all Subnets in the VPC
echo "Listing all subnets inside VPC $vpc_id"
aws ec2 describe-subnets --filters Name=vpc-id,Values=$vpc_id --query 'Subnets[*].[SubnetId, CidrBlock]'
echo ______________________________________________________________

# Show all NAT Gateways in the VPC
echo "Listing all NAT Gateways inside VPC $vpc_id"
aws ec2 describe-nat-gateways --filters Name=vpc-id,Values=$vpc_id --query 'NatGateways[*].[NatGatewayId, VpcId, SubnetId, PublicIp]'
echo ______________________________________________________________

# Show all Customer Gateways 
echo "Listing all Customer Gateways inside VPC $vpc_id"
aws ec2 describe-customer-gateways --filters Name=vpc-id,Values=$vpc_id --query 'CustomerGateways[*].[CustomerGatewayId, VpcId]'
echo ______________________________________________________________

# Show all Route Tables in the VPC
echo "Listing all Route Tables inside VPC $vpc_id"
aws ec2 describe-route-tables --filters Name=vpc-id,Values=$vpc_id --query 'RouteTables[*].[RouteTableId, VpcId]'
echo ______________________________________________________________

# Show all VPC Peering Connections in the VPC
echo "Listing all VPC Peering Connections inside VPC $vpc_id"
aws ec2 describe-vpc-peering-connections --filters Name=vpc-id,Values=$vpc_id --query 'VpcPeeringConnections[*].[VpcId, PeeringConnectionId, PeerVpcId]'
echo ______________________________________________________________

# Show all Endpoints in the VPC
echo "Showing all Endpoints inside VPC $vpc_id"
aws ec2 describe-vpc-endpoints --filters Name=vpc-id,Values=$vpc_id --query 'Endpoints[*].[EndpointId, VpcId, ServiceName]'
echo ______________________________________________________________

# Show all Network ACLS in the VPC
echo "Showing all Network ACLS inside VPC $vpc_id"
aws ec2 describe-network-acls --filters Name=vpc-id,Values=$vpc_id --query 'NetworkAcls[*].[NetworkAclId, VpcId]'
echo ______________________________________________________________

# List all Transit Gateways
echo "Showing all Transit Gateways inside VPC $vpc_id"
aws ec2 describe-transit-gateways --filters Name=vpc-id,Values=$vpc_id --query 'TransitGateways[*].[TransitGatewayId, VpcId]'
echo ______________________________________________________________

# List all VPN connections in the VPC
echo "Showing all VPN connections inside VPC $vpc_id"
aws ec2 describe-vpn-connections --filters Name=vpc-id,Values=$vpc_id --query 'VpnConnections[*].[VpcId, VpnConnectionId, VpnGatewayId, VpcId]'
echo ______________________________________________________________

# Show all Elastic IPs in the VPC
echo "Showing all Elastic IPs inside VPC $vpc_id"
aws ec2 describe-addresses --filters Name=vpc-id,Values=$vpc_id --query 'Addresses[*].[PublicIp, AllocationId]'
echo ______________________________________________________________

# List all EC2 instances in the VPC
echo "Listing all EC2 instances inside VPC $vpc_id"
aws ec2 describe-instances --filters Name=vpc-id,Values=$vpc_id --query 'Reservations[*].Instances[*].[InstanceId, InstanceType, PublicIpAddress, PrivateIpAddress]'
echo ______________________________________________________________

# List all EBS volumes in the VPC
echo "Listing all EBS volumes inside VPC $vpc_id"
aws ec2 describe-volumes --filters Name=vpc-id,Values=$vpc_id --query 'Volumes[*].[VolumeId, Size, AvailabilityZone]'
echo ______________________________________________________________

# List all EBS snapshots in the VPC
echo "Listing all EBS snapshots inside VPC $vpc_id"
aws ec2 describe-snapshots --filters Name=vpc-id,Values=$vpc_id --query 'Snapshots[*].[SnapshotId, VolumeId, StartTime]'
echo ______________________________________________________________

# List all Flow Logs
echo "Listing all Flow Logs inside VPC $vpc_id"
aws ec2 describe-flow-logs --filter "Name=vpc-id,Values=$vpc_id" --query 'FlowLogs[*].[FlowLogId, VpcId, LogDestination, LogFormat, LogDestinationType]'
echo ______________________________________________________________