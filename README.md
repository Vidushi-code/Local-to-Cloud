# Local-to-Cloud File Backup Using AWS S3

A cloud project that backs up files from a local folder to an Amazon S3 bucket using a Python (boto3) script. It demonstrates a basic **hybrid-cloud use case**: data kept on a local (on-premises) machine is protected by a copy in the public cloud.

## Overview

If a laptop or local server fails, the files on it are lost. This project keeps a copy of those files in AWS S3, so they can be listed and restored whenever needed. Access is handled through a dedicated IAM user instead of the root account, and S3 versioning keeps older copies of files that get overwritten.

## Architecture

```
┌──────────────────┐   Python (boto3)   ┌───────────────────────┐
│  Local folder    │ ─────────────────► │  Amazon S3 bucket     │
│  (my_local_folder)│  upload / list /  │  (versioning enabled) │
│                  │ ◄───────────────── │  Region: ap-south-1   │
└──────────────────┘     download       └───────────────────────┘
          ▲
          │ credentials via AWS CLI (IAM user, limited permissions)
```

## Features

- Upload all files from a local folder to an S3 bucket
- List the files stored in the bucket along with their sizes
- Download (restore) a file from S3 back to the local machine
- S3 versioning enabled, so older versions of a file are retained
- Uses an IAM user with limited S3 permissions instead of the root account

## Tech Stack

| Tool | Purpose |
|------|---------|
| AWS S3 | Cloud object storage for backups |
| AWS IAM | Secure, limited-permission access |
| AWS CLI | Configure credentials locally |
| Python 3 + boto3 | Script to talk to S3 |

## Project Structure

```
local-to-cloud-project/
├── backup.py            # Main script (upload, list, download)
├── requirements.txt     # Python dependencies
├── my_local_folder/     # Sample files to back up
├── screenshots/         # Proof of working project
├── .gitignore
└── README.md
```

## Prerequisites

- An AWS account (Free Tier is enough)
- Python 3.8 or higher
- AWS CLI installed

## Setup

1. **Create an S3 bucket** (General purpose) in the `ap-south-1` (Mumbai) region and enable **Bucket Versioning** under Properties.
2. **Create an IAM user** (no console access) and attach an S3 permissions policy. Generate an access key for CLI use.
3. **Configure the AWS CLI:**
   ```bash
   aws configure
   ```
   Enter the access key, secret key, region `ap-south-1` and output format `json`.
4. **Verify the connection:**
   ```bash
   aws s3 ls
   ```
5. **Install dependencies** (a virtual environment is recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   pip install -r requirements.txt
   ```
6. **Set your bucket name** in `backup.py`:
   ```python
   BUCKET = "your-bucket-name"
   ```

## Usage

```bash
python backup.py
```

The script uploads every file from `my_local_folder`, prints the files stored in the bucket with their sizes, and downloads `notes.txt` as `restored_notes.txt`.

### Sample output

```
Uploaded: file1.txt
Uploaded: file2.txt
Uploaded: notes.txt
file1.txt 9
file2.txt 9
notes.txt 9
Downloaded: notes.txt
```

## Versioning Demo

1. Edit `notes.txt` and run the script again.
2. In the S3 console, open `notes.txt` and go to the **Versions** tab.
3. Both the old and the new version are available, so an overwritten file can be recovered.

## Screenshots

| S3 bucket with files | Versioning (Versions tab) | Terminal output |
|---|---|---|
| ![bucket](screenshots/s3-bucket-files.png) | ![versions](screenshots/s3-versions.png) | ![terminal](screenshots/terminal-output.png) |

## Security Practices

- Used a dedicated IAM user instead of the root account
- Console access disabled for the IAM user (CLI only)
- Bucket is private (Block all public access is ON)
- Credentials are stored by AWS CLI on the local machine, never in code
- `.gitignore` excludes the virtual environment and any credential files

## Limitations

- Uploads only top-level files (subfolders are skipped)
- Re-uploads all files on every run instead of only changed ones
- Basic script without error handling
- Runs manually, with no scheduling

## Future Improvements

- Support nested folders and upload only changed files
- Add error handling (try/except) and logging
- Schedule automatic backups (Task Scheduler or cron)
- Add S3 lifecycle rules to move old backups to cheaper storage classes
- Restrict the IAM policy to a single bucket

## Learning Outcomes

- S3 buckets, objects and versioning
- IAM users, access keys and the least-privilege principle
- Using the AWS CLI and boto3 from Python
- How a local-to-cloud backup works in a hybrid-cloud setup

## Author

**Vidushi Agarwal**