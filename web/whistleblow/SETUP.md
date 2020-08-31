
# First Bucket

## Solve

Player deduces that bucket is setup with `authenticated-read` as part of its ACL.

```
# ...authenticate as AWS user

# get link to access files
$ aws s3 ls s3://ad586b62e3b5921bd86fe2efa4919208/...

# ... find path to all necessary components

# get presigned link to relevant paths
$ aws s3 presign s3://ad586b62e3b5921bd86fe2efa4919208/...
```

## Setup

Create a new IAM user that has read access to objects and buckets in S3.

### Second Bucket

We do this first in order to generate the info needed for the

Create a bucket that does not have public-read priviledge. It should in the Ohio region (`us-east-2`).

Give access only to the IAM user with S3 read priviledge created earlier.

It is now configured only for access in an Ohio-based EC2 instance, with the proper credentials. Create a new presigned URL for distribution

```
$ aws s3 presign s3://super-top-secret-dont-look/.sorry/.for/.nothing/flag.txt --expires-in 180000
https://super-top-secret-dont-look.s3.amazonaws.com/.sorry/.for/.nothing/flag.txt?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAQHTF3NZUVXKMS6HL%2F20200831%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20200831T020639Z&X-Amz-Expires=18000&X-Amz-SignedHeaders=host&X-Amz-Signature=515ad736e5f2068b2605be97e2ced10e23fb993fbadcc697f522564e2e0d3386
```



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

These objects contain necessary components for the next bucket: next bucket name, access key, path, signature. They figure out the date from the description.
