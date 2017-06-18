import boto3
import MySQLdb
import peewee
from peewee import *

aws_id = raw_input("Enter AWS Access Key ID: ")
secret_key = raw_input("Enter AWS Secret Access Key: ")

# aws_id = 'AKIAJ67OSJZZKLGB2HMA'
# secret_key = '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'

ec2 = boto3.client(
    'ec2',
    aws_access_key_id=aws_id,
    aws_secret_access_key=secret_key
)

response = ec2.describe_instances()
instances = response['Reservations'][0]['Instances']

db = MySQLDatabase('ec2_info', user='root',passwd='guitar677')

class Instance(peewee.Model):
    instanceId = peewee.CharField()
    instanceType = peewee.CharField()
    zone = peewee.CharField()

    class Meta:
        database = db

db.connect()

for x in instances:
    new = Instance(instanceId=x['InstanceId'], instanceType=x['InstanceType'], zone=x['Placement']['AvailabilityZone'])
    new.save()

for instance in Instance.select():
    print "\n", "Instance ID: ", instance.instanceId, "\n", "Instance Type: ", instance.instanceType, "\n", "Zone :", instance.zone

db.close()
