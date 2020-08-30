
# First Bucket

## Solve

Player deduces that bucket is setup with `authenticated-read` as part of its ACL.

```
# ...authenticate as AWS user

# get link to access files
$ aws s3 ls s3://ad586b62e3b5921bd86fe2efa4919208/...

# ... find path to all necessary components

# get presigned link to path
$ aws s3 presign s3://ad586b62e3b5921bd86fe2efa4919208/...
```

## Setup

Create a new IAM user that has read access to objects and buckets in S3.

### First Bucket

Create a bucket that has `authenticated-read` in the Northern California region (`us-west-1`). Bucket should first
be made public in order to set ACL:

```
$ aws put-bucket-acl --bucket <BUCKET> --acl authenticated-read
```


Run the following script to create layers of bogus directories and files. Credentials needed for next bucket are hidden
amongst them. All objects will also have `authenticated-read`:

```
$ python init_bucket.py
```

The information that is dispersed should be stored in `solve.txt`.

These objects contain necessary components for the next bucket: next bucket name, access key, and secret.

### Second Bucket

Create a bucket that does not have public-read priviledge. It should in the Ohio region (`us-east-2`).

Give access only to the IAM user with S3 read priviledge created earlier. Set the bucket policy based on `bucket_policy.json`.

It is now configured only for access in an Ohio-based EC2 instance, with the proper credentials.
