# ebs-snapshot

Making EBS snapshot script written in Python.

## Installation

Just download `ebs_snapshot.py` on your AWS instance and set its permission to 755.

### AmazonLinux

On Amazonlinux, modules are installed by default.
If you don't use system Python, install `boto` and `requests` on your Python environment.

### Ubuntu

Use apt-get(modules will be installed on system Python) or install `boto` and `requests` by yourself.

```
apt-get update
apt-get install awscli python-pip python-boto
```

## AWS Credentials

Set AWS credential by environment variable or create `~/.boto`.

* environment variable

```
export AWS_ACCESS_KEY_ID=xxxxx
export AWS_SECRET_ACCESS_KEY=xxxxx
```

* ~/.boto

```
[Credentials]
aws_access_key_id=xxxxx
aws_secret_access_key=xxxxx
```

Note: the credential need some IAM policies. The following is example.

* IAM policy example

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:Describe*",
                "ec2:CreateSnapshot",
                "ec2:DeleteSnapshot"
            ],
            "Resource": "*"
        }
    ]
}
```

## Usage

Execute `ebs_snapshot.py` on the instance which you would like to create EBS snapshot.

* options
  - -h: show helps
  - -n: The number of snapshot generations. default: 3
  - -l: The log file path. default: /tmp/ebs_snapshot.log


## License

MIT
