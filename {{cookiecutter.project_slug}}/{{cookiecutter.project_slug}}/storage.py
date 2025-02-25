{%- if cookiecutter.cloud_provider == 'AWS' -%}
from storages.backends.s3boto3 import S3Boto3Storage


class StaticRootS3Boto3Storage(S3Boto3Storage):
    location = "static"
    default_acl = "public-read"


class MediaRootS3Boto3Storage(S3Boto3Storage):
    location = "media"
    file_overwrite = False
{%- elif cookiecutter.cloud_provider == 'Azure' %}
from storages.backends.azure_storage import AzureStorage


class PublicAzureStorage(AzureStorage):
    expiration_secs = None
{%- endif %}
