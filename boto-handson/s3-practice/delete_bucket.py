import boto3

def delete_bucket_objects(s3_connection, bucket_name):
    response = s3_connection.list_objects_v2(Bucket=bucket_name)
    objects = response.get('Contents', [])
    if objects:
        delete_keys = {'Objects': [{'Key': obj['Key']} for obj in objects]}
        s3_connection.delete_objects(Bucket=bucket_name, Delete=delete_keys)


def delete_bucket(bucket_name):
    s3_client = boto3.client('s3')
    
    delete_bucket_objects(s3_client, bucket_name)
    s3_client.delete_bucket(Bucket=bucket_name)
    

if __name__=='__main__':
    from list_buckets import list_buckets_resource
    for bucket in list_buckets_resource():
        delete_bucket(bucket)