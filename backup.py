import boto3, os

BUCKET = "local-to-cloud-storage"
s3 = boto3.client("s3")

def upload_folder(folder):
    for name in os.listdir(folder):
        path = os.path.join(folder, name)
        if os.path.isfile(path):
            s3.upload_file(path, BUCKET, name)
            print("Uploaded:", name)

def list_files():
    resp = s3.list_objects_v2(Bucket=BUCKET)
    for obj in resp.get("Contents", []):
        print(obj["Key"], obj["Size"])

def download_file(name, dest):
    s3.download_file(BUCKET, name, dest)
    print("Downloaded:", name)

if __name__ == "__main__":
    upload_folder("my_local_folder")
    list_files()
    download_file("notes.txt", "restored_notes.txt")