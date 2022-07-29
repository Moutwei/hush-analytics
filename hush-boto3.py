import boto3

# create bucket
# sess = boto3.Session(region_name='us-east-1')
# s3client = sess.client('s3')
#
# bucket_name = 'hush-bucket-test1'
#
# s3client.create_bucket(Bucket=bucket_name)

# HIDE CREDENTIALS install awscli then configure
s3 = boto3.resource('s3',aws_access_key_id='AKIAVMCU5DXBJOQGMTEO', aws_secret_access_key='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')

# print my buckets
for each_b in s3.buckets.all():
    print(each_b.name)

# add file to bucket
s3.meta.client.upload_file('stats.csv','hush-bucket-test1', 'stats.csv')
