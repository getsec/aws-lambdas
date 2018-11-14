import json
import boto3
import logging
from botocore.exceptions import ClientError
logger = logging.getLogger()
logger.setLevel(logging.INFO)
client = boto3.client('s3')
bucket_list = []

def put_bucket_encryption(bucket,client):
  encrypt = client.put_bucket_encryption(
    Bucket=bucket,
    ServerSideEncryptionConfiguration={
        'Rules': [
            {
                'ApplyServerSideEncryptionByDefault': {
                    'SSEAlgorithm': 'AES256'
                }
            },
        ]
    }
  )
  return encrypt

def get_bucket_list(client):
  response = client.list_buckets()
  for i in response['Buckets']:
    bucket_list.append(i['Name'])
  return bucket_list


def lambda_handler(event, context):
    for bucket in get_bucket_list(client):
      try:
        bucket_encryption = client.get_bucket_encryption( Bucket=bucket )
      except ClientError as error:
        put_bucket_encryption(bucket, client)
        logging.info("{} does not have encryption. Adding".format(bucket))
      except TypeError as type:
        pass

    return True