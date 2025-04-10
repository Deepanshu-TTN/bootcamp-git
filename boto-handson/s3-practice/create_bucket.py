import boto3
import boto3.session
import uuid


'''
create bucket kwargs:
    ACL='private'|'public-read'|'public-read-write'|'authenticated-read',
    Bucket='string',
    CreateBucketConfiguration={
        'LocationConstraint': 'af-south-1'|'ap-east-1'|'ap-northeast-1'|'ap-northeast-2'|'ap-northeast-3'|'ap-south-1'|'ap-south-2'|'ap-southeast-1'|'ap-southeast-2'|'ap-southeast-3'|'ap-southeast-4'|'ap-southeast-5'|'ca-central-1'|'cn-north-1'|'cn-northwest-1'|'EU'|'eu-central-1'|'eu-central-2'|'eu-north-1'|'eu-south-1'|'eu-south-2'|'eu-west-1'|'eu-west-2'|'eu-west-3'|'il-central-1'|'me-central-1'|'me-south-1'|'sa-east-1'|'us-east-2'|'us-gov-east-1'|'us-gov-west-1'|'us-west-1'|'us-west-2',
        'Location': {
            'Type': 'AvailabilityZone'|'LocalZone',
            'Name': 'string'
        },
        'Bucket': {
            'DataRedundancy': 'SingleAvailabilityZone'|'SingleLocalZone',
            'Type': 'Directory'
        }
    },
    GrantFullControl='string',
    GrantRead='string',
    GrantReadACP='string',
    GrantWrite='string',
    GrantWriteACP='string',
    ObjectLockEnabledForBucket=True|False,
    ObjectOwnership='BucketOwnerPreferred'|'ObjectWriter'|'BucketOwnerEnforced'
'''

def create_bucket_name(bucket_prefix):
    '''add a random string to end of the prefix'''
    return ''.join([bucket_prefix, str(uuid.uuid4())])


def create_bucket_using_client(bucket_name):
    '''Create a bucket and return Json Client Response'''
    session = boto3.session.Session()
    location = {'LocationConstraint': session.region_name}
    
    s3_client = boto3.client('s3')
    
    response = s3_client.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration = location
    )
    
    return response


def create_bucket_using_resource(bucket_name):
    '''Create a bucket and return the Bucket Object'''
    session = boto3.session.Session()
    location = {'LocationConstraint': session.region_name}
    
    s3_resource = boto3.resource('s3')
    
    bucket = s3_resource.Bucket(bucket_name)
    
    bucket.create(
        CreateBucketConfiguration = location
    )
    
    return bucket


if __name__ == '__main__':
    # name = create_bucket_name('bucket-client-')
    
    # response = create_bucket_using_client(name)
    # print(response)
    
    name = create_bucket_name('bucket-resource-')
    bucket = create_bucket_using_resource(name)
    print(bucket)