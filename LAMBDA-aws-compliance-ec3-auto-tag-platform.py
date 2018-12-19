import boto3
import json
import os
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
## The naming convention of the windows servers

ec2 = boto3.client('ec2')
all_instances = ec2.describe_instances()


def lambda_handler(event, context):

  ## we need these to get the name of the instance, if lin or win in the name we can tag the platform
  windows_tag = os.environ["windows_instance_name_key"]
  linux_tag = os.environ["linux_instance_name_key"]

  ## Function that takes instance id and tags as windows
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

  ## Functionthat takes instance id and tags as linux
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

  ## this loops through all the instances
  for reservation in all_instances["Reservations"] :
    for instance in reservation["Instances"]:
      for tag in instance["Tags"]:

        ## Get current instance ID
        instance_id = instance["InstanceId"]

        ## will use later if the instance is already tagged
        return_already_tagged = "Instance ID {} already tagged with platform TAG".format(instance_id)

        ## if the platform key is already linux or windows, we would like to stop running the script for that instance
        ## Or there will just be a lot of logs :(
        if tag["Key"] == "platform":
          if 'linux' in tag["Value"]:
            logging.info("Instance ID {} already tagged with linux platform".format(instance_id))
          if 'windows' in tag["Value"]:
            logging.info("Instance ID {} already tagged with windows platform".format(instance_id))

        ## Then we look at the name tag and see if win or lin is in the name then execute the tagging function(s)
        if tag["Key"] == "Name":
          if linux_tag in tag["Value"]:
            logging.info("Instance ID {} with name 'lin' found in name tag. Tagging instance with linux platform".format(instance_id))
            tag_instance_linux(ec2,instance_id)
          if windows_tag in tag["Value"]:
            tag_instance_windows(ec2,instance_id)
            logging.info("Instance ID {} with name 'win' found in name tag. Tagging instance with windows platform".format(instance_id))