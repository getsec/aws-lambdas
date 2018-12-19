# -*- coding: utf-8 -*-
import boto3
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('iam')

owner_tag_name = os.environ['owner_tag_name']

def auto_tag_iam_user(username, created_by, client, owner_tag_name):
  response = client.tag_user(
    UserName=username,
    Tags=[
        {
            'Key': owner_tag_name,
            'Value': created_by
        },
    ]
  )
  logger.info(f"User: '{username}' created_by: '{created_by}'")
  return response

def auto_tag_iam_role(rolename, created_by, client, owner_tag_name):
  response = client.tag_role(
    RoleName=rolename,
    Tags=[
        {
            'Key': owner_tag_name,
            'Value': created_by
        },
    ]
  )
  logger.info(f"Role: '{rolename}' created_by: '{created_by}'")
  return response

def lambda_handler(event, context):
  # If the event is a create user make sure to invoke the tag_user function
  if event['detail']['eventName'] == 'CreateUser':
    username = event['detail']['requestParameters']['userName']
    created_by = event['detail']['userIdentity']['arn'].split('/')[-1]
    auto_tag_iam_user(username, created_by, client, owner_tag_name)
  # If the event is a create role make sure to invoke the tag_role function
  elif event['detail']['eventName'] == 'CreateRole':
    rolename = event['detail']['requestParameters']['roleName']
    created_by =  event['detail']['userIdentity']['arn'].split('/')[-1]
    auto_tag_iam_role(rolename, created_by, client, owner_tag_name)


