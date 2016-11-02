import boto3 as aws
import botocore

from shuttl import app

## Class for AWS S3 storage
class Storage:

    bucket = None ##< the bucket the file belongs to
    s3 = aws.resource("s3")  ##< The s3 instance

    @classmethod
    def GetBucket(cls, bucketName):
        cls.bucket = cls.s3.Bucket(bucketName)
        pass

    @classmethod
    def Upload(cls, fileObj):
        if app.config["TESTING"]:
            return
        if cls.bucket is None:
            cls.GetBucket("shuttl.io")
        return cls.bucket.upload_file(fileObj.filePath, fileObj.filePath)

    @classmethod
    def Delete(cls, fileObj, bucketName="shuttl.io"):
        if app.config["TESTING"]:
            return
        try:
            obj = cls.s3.Object(bucketName, fileObj.filePath)
            return obj.delete()
        except botocore.exceptions.ClientError:
            pass
        pass

    @classmethod
    def Download(cls, fileObj, bucketName="shuttl.io"):
        if app.config["TESTING"]:
            return
        try:
            obj = cls.s3.Object(bucketName, fileObj.filePath)
            return obj.download_file(fileObj.filePath)
        except botocore.exceptions.ClientError:
            raise FileNotFoundError("No such file or directory: {}".format(fileObj.filePath))
        pass