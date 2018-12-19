import boto3
from botocore.exceptions import ClientError
import json
import sys
import os
import logging
import boto3

client = boto3.client("ec2")

security_group_id = event["detail"]["requestParameters"]["groupId"]
ip_permissions = event["detail"]["requestParameters"]["ipPermissions"]


def remove_ingress(security_group_id, client):
  response = client.revoke_security_group_ingress(
    GroupId=security_group_id,
    IpPermissions = ip_permissions["items"]
  )
  return response

print(remove_ingress(security_group_id,client))
