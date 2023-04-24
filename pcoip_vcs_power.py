import boto3
import json

regions = ["us-east-1", "us-west-2"]


def paginate(method, **kwargs):
    client = method.__self__
    paginator = client.get_paginator(method.__name__)
    for page in paginator.paginate(**kwargs).result_key_iters():
        for result in page:
            yield result


for region in regions:
    workspaces = boto3.client("workspaces", region_name=region)
    for workspace in paginate(workspaces.describe_workspaces):
        if workspace["BundleId"] == "wsb-6m4xgd4tz":
            print(
                f"{workspace['UserName']}| {workspace['WorkspaceId']} | {workspace['BundleId']} |{region} "
            )


# wsb-6m4xgd4tz
