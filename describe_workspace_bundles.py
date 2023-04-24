import boto3
import os
import csv

regions = ["us-east-1", "us-west-2"]
directory = "."


def paginate(method, **kwargs):
    client = method.__self__
    paginator = client.get_paginator(method.__name__)
    for page in paginator.paginate(**kwargs).result_key_iters():
        for result in page:
            yield result


with open(
    os.path.join(directory, "describe_workspace_bundles.csv"), "w", newline=""
) as file:
    writer = csv.writer(file)

    writer.writerow(["BundleId", "ImageId", "Name"])

    for region in regions:
        workspaces = boto3.client("workspaces", region_name=region)
        for workspace in paginate(workspaces.describe_workspace_bundles):
            writer.writerow(
                [workspace["BundleId"], workspace["ImageId"], workspace["Name"]]
            )
