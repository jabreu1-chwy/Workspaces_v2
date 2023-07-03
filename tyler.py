import boto3
import json


def get_workspace(workspaces, id):
    response = workspaces.describe_workspaces(
        WorkspaceIds=[
            id,
        ]
    )
    print(json.dumps(response, default=str, indent=4))


# view workspaces in region named us-east-1. boto3.client connects to AWS data


def main():
    ids = ["A", "B"]
    for id in ids:
        workspaces = boto3.client("workspaces", region_name="us-east-1")
        get_workspace(workspaces)


main()


ids = ["real_ws", "real_ws", "fake_ws"]
regions = ["us-east-1", "us-west-2"]
for region in regions:
    for id in ids:
        found_id = False
        try:
            if id in region:
                found_id = True
                print("workspace is found in" + region)
        except Exception as e:
            print(f"Error: {e}")
