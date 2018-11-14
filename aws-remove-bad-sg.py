import boto3
from botocore.exceptions import ClientError
import json
import sys
import os
import logging


def lambda_handler(event,context):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    ## first determin if instance is whitlisted
    whitelist = os.environ["whitelist_instance_ids"]
    if ',' in whitelist:
      whitelist = whitelist.split(",")
      for i in whitelist:
        if event["detail"]["instance-id"] == i:
          logging.info("[EXIT] Matched whitelist item: {}".format(i))
          return "[EXIT] Matched whitelist item: {}".format(i)
    else:
      whitelist = os.environ["whitelist_instance_ids"]
      if event["detail"]["instance-id"] == whitelist:
        logging.info("[EXIT] Matched whitelist item: {}".format(whitelist))
        return "[EXIT] Matched whitelist item: {}".format(whitelist)


    group_ids = []
    logging.info(whitelist)
    client = boto3.client('ec2')

    def get_id_from_event(event):
      instance_id = event["detail"]["instance-id"]
      return instance_id

    def get_sg_id_from_instance(instance_id, client):
      instance_sg_set = set()
      sg_set = set()
      response = client.describe_instances(
            InstanceIds=[
            instance_id
        ]
      )
      for reservation in response["Reservations"] :
        for instance in reservation["Instances"]:
          for sg in instance["SecurityGroups"]:
            instance_sg_set.add(sg["GroupId"])
      return instance_sg_set

    def remove_sg_ingress(client, security_group_ids):
      responses = []
      for group in security_group_ids:
        try:
          response = client.revoke_security_group_ingress(
          GroupId = group,
          IpProtocol = 'tcp',
          FromPort = 22,
          ToPort = 22,
          CidrIp = '0.0.0.0/0'
          )
          responses.append(response)
          logging.info("Deleting open ingress rule for group: {}".format(group))
        except ClientError as e:
          logging.info(e)
          pass
      return responses

    instance_id = get_id_from_event(event)
    security_group_ids = get_sg_id_from_instance(instance_id, client)
    try:
      remove_sg = remove_sg_ingress(client, security_group_ids)
    except ClientError as e:
      logging.info("shit")

    return remove_sg

