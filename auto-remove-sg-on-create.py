import boto3
from botocore.exceptions import ClientError
import json
import sys
import os
import logging
import boto3

client = boto3.client("ec2")
event = {
  "version": "0",
  "id": "6570517a-dc3f-57ea-e1f5-1e280a7986ee",
  "detail-type": "AWS API Call via CloudTrail",
  "source": "aws.ec2",
  "account": "956884876709",
  "time": "2018-11-14T19:53:49Z",
  "region": "ca-central-1",
  "resources": [],
  "detail": {
    "eventVersion": "1.05",
    "userIdentity": {
      "type": "AssumedRole",
      "principalId": "AROAILH5H46QMBNKTLARU:ngetty@wawanesa.com",
      "arn": "arn:aws:sts::956884876709:assumed-role/AWSReservedSSO_AdministratorAccess_d5947e17ce774e79/ngetty@wawanesa.com",
      "accountId": "956884876709",
      "accessKeyId": "ASIA55SWIPWS7W27VRVG",
      "sessionContext": {
        "attributes": {
          "mfaAuthenticated": "false",
          "creationDate": "2018-11-14T19:11:27Z"
        },
        "sessionIssuer": {
          "type": "Role",
          "principalId": "AROAILH5H46QMBNKTLARU",
          "arn": "arn:aws:iam::956884876709:role/aws-reserved/sso.amazonaws.com/AWSReservedSSO_AdministratorAccess_d5947e17ce774e79",
          "accountId": "956884876709",
          "userName": "AWSReservedSSO_AdministratorAccess_d5947e17ce774e79"
        }
      }
    },
    "eventTime": "2018-11-14T19:53:49Z",
    "eventSource": "ec2.amazonaws.com",
    "eventName": "AuthorizeSecurityGroupIngress",
    "awsRegion": "ca-central-1",
    "sourceIPAddress": "64.4.90.120",
    "userAgent": "console.ec2.amazonaws.com",
    "requestParameters": {
      "groupId": "sg-06c3c83ed95189abb",
      "ipPermissions": {
        "items": [
          {
            "ipProtocol": "tcp",
            "fromPort": 22,
            "toPort": 22,
            "groups": {},
            "ipRanges": {
              "items": [
                {
                  "cidrIp": "123.123.123.123/32"
                }
              ]
            },
            "ipv6Ranges": {},
            "prefixListIds": {}
          },
          {
            "ipProtocol": "tcp",
            "fromPort": 0,
            "toPort": 0,
            "groups": {},
            "ipRanges": {
              "items": [
                {
                  "cidrIp": "0.0.0.0/0"
                }
              ]
            },
            "ipv6Ranges": {},
            "prefixListIds": {}
          }
        ]
      }
    },
    "responseElements": {
      "requestId": "8377805e-4daf-4c12-975e-6c860f9b43be",
      "_return": "True"
    },
    "requestID": "8377805e-4daf-4c12-975e-6c860f9b43be",
    "eventID": "012b7e01-c32e-4cce-8ca1-2ce351ecb3aa",
    "eventType": "AwsApiCall"
  }
}

security_group_id = event["detail"]["requestParameters"]["groupId"]
ip_permissions = event["detail"]["requestParameters"]["ipPermissions"]


def remove_ingress(security_group_id, client):
  response = client.revoke_security_group_ingress(
    GroupId=security_group_id,
    IpPermissions = ip_permissions["items"]
  )
  return response

print(remove_ingress(security_group_id,client))
