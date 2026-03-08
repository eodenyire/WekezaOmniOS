import boto3

class S3Backend:

    def __init__(self, bucket):
        self.s3 = boto3.client("s3")
        self.bucket = bucket

    def save(self, snapshot_path, snapshot_id):

        for file in snapshot_path:

            self.s3.upload_file(
                file,
                self.bucket,
                f"{snapshot_id}/{file}"
            )

    def load(self, snapshot_id):

        return f"s3://{self.bucket}/{snapshot_id}"
