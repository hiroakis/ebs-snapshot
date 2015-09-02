# ebs-snapshot

Making EBS snapshot script written in Python.

# Installation

Just download `ebs_snapshot.py` on your AWS instance and set its permission to 755.

## On AmazonLinux

On amazonlinux, modules are installed by default.
If you don't use system Python, install `boto` and `requests` on your Python environment.

## On Ubuntu

Use apt-get(modules will be installed on system Python) or install `boto` and `requests` by yourself.

```
apt-get update
apt-get install awscli python-pip python-boto
```

# Usage

Execute `ebs_snapshot.py` on the instance which you would like to create EBS snapshot.

* options
  - -h: show helps
  - -n: The number of snapshot generations. default: 3
  - -l: The log file path. default: /tmp/ebs_snapshot.log

# License

MIT
