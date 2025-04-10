import boto3

def list_buckets_client():
    s3_client = boto3.client('s3')
    buckets = s3_client.list_buckets()['Buckets']
    return [bucket['Name'] for bucket in buckets]
    
    
def list_buckets_resource():
    s3_resource = boto3.resource('s3')
    buckets = [bucket.name for bucket in s3_resource.buckets.all()]
    return buckets


if __name__ == '__main__':
    print(list_buckets_client())
    print(list_buckets_resource())