import boto3
import json
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

ec2 = boto3.client('ec2')
all_instances = ec2.describe_instances()



def tag_instance_windows(ec2,instance_id):
  response = ec2.create_tags(
    Resources=[
        instance_id,
    ],
    Tags=[
        {
            'Key': 'platform',
            'Value': 'windows'
        },
    ]
  )

def tag_instance_linux(ec2,instance_id):
  response = ec2.create_tags(
    Resources=[
        instance_id,
    ],
    Tags=[
        {
            'Key': 'platform',
            'Value': 'linux'
        },
    ]
  )

for reservation in all_instances["Reservations"] :
  for instance in reservation["Instances"]:
    for tag in instance["Tags"]:

      instance_id = instance["InstanceId"]
      return_already_tagged = "Instance ID {} already tagged with platform TAG".format(instance_id)

      if tag["Key"] == "platform":
        if 'linux' in tag["Value"]:
          logger.info("Instance ID {} already tagged with linux platform".format(instance_id))
        if 'windows' in tag["Value"]:
          logger.info("Instance ID {} already tagged with windows platform".format(instance_id))
      if tag["Key"] == "Name":
        if 'lin' in tag["Value"]:
          logger.info("Instance ID {} with name 'lin' found in name tag. Tagging instance with linux platform".format(instance_id))
          tag_instance_linux(ec2,instance_id)
        if 'win' in tag["Value"]:
          tag_instance_windows(ec2,instance_id)
          logger.info("Instance ID {} with name 'win' found in name tag. Tagging instance with windows platform".format(instance_id))




