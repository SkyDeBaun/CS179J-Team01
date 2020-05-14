import time
from boto3.s3.transfer import S3Transfer
import boto3

def getTimeStamp():
  return str(time.strftime("%Y-%m-%d_%H:%M:%S"))


def getAWSCredentials():
  accessKeysFile = open('../Certificates/accessKeys.txt', 'r')
  accessKey = accessKeysFile.readline().strip()
  secretKey = accessKeysFile.readline().strip()
  accessKeysFile.close()
  if (not accessKey or not secretKey):
    print("Keys unable to be imported")
    exit(1)
  return (accessKey, secretKey)

def uploadToS3(fileToUploadPath, bucketName, accessKeys): #access key from tuple from getAWSCredentials
  client = boto3.client('s3', aws_access_key_id=accessKeys[0],aws_secret_access_key=accessKeys[1])
  transfer = S3Transfer(client)
  transfer.upload_file(fileToUploadPath, bucketName, fileToUploadPath[3:]) # Second filepath is on the bucket server

def otherUpload(fileToUploadPath, bucketName, accessKeys):
  session = boto3.Session(
    region_name = 'us-west-1',
    aws_access_key_id=accessKeys[0],
    aws_secret_access_key=accessKeys[1],
  )
  s3 = session.resource('s3')
# Filename - File to upload
# Bucket - Bucket to upload to (the top level directory under AWS S3)
# Key - S3 object name (can contain subdirectories). If not specified then file_name is used
  s3.meta.client.upload_file(Filename=fileToUploadPath, Bucket=bucketName, Key=fileToUploadPath[3:])
