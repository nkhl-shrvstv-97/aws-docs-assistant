import os
import glob
import boto3
from botocore.exceptions import ClientError
from backend.ingestion.download_docs import download_and_process_docs

def upload_files_to_s3(bucket_name):
    s3_client = boto3.client("s3")
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "docs"))
    md_files = glob.glob(os.path.join(data_dir, "*.md"))

    if not md_files:
        print("No markdown files found to upload. Ensure download_docs finished successfully.")
        return

    print(f"Uploading {len(md_files)} files to S3 bucket: {bucket_name}...")
    for filepath in md_files:
        filename = os.path.basename(filepath)
        try:
            s3_client.upload_file(filepath, bucket_name, filename)
            print(f"Uploaded: {filename}")
        except ClientError as e:
            print(f"Failed to upload {filename} to S3: {e}")
            return
    print("All uploads complete! This will trigger the AWS SQS and Lambda ingestion pipeline.")

def main():
    # 1. Download and process the target documentation URLs locally
    print("Step 1: Downloading and converting AWS Documentation URLs...")
    download_and_process_docs()

    # 2. Upload to S3 landing bucket
    bucket_name = os.environ.get("S3_BUCKET_NAME")
    if not bucket_name:
        print("\nError: S3_BUCKET_NAME environment variable is not set.")
        print("Please set it in your environment or .env file, e.g.:")
        print("export S3_BUCKET_NAME=nikhil-aws-docs-assistant-landing-f2b7a9c8")
        return

    print("\nStep 2: Uploading markdown files to S3...")
    upload_files_to_s3(bucket_name)

if __name__ == "__main__":
    main()
