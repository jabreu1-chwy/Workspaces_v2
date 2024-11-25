import boto3
import time
import csv
from botocore.exceptions import ClientError

regions = ["us-east-1", "us-west-2"]
processed_ids = []
processed_count = 0

with open(
    "/Users/jabreu1/Library/CloudStorage/OneDrive-Chewy.com,LLC/Documents/Workspaces/rebuild_workspaces.csv",
    newline="",
    encoding="utf-8-sig",
) as inputfile:
    workspace_ids = [row[0] for row in csv.reader(inputfile)]

for workspace_id in workspace_ids:
    found = False

    for region in regions:
        if workspace_id in processed_ids:
            continue

        try:
            # checks if it exists first
            checking_ws = boto3.client(
                "workspaces", region_name=region
            ).describe_workspaces(WorkspaceIds=[workspace_id])
            if not checking_ws["Workspaces"]:
                continue
            found = True
            rebuild_ws = boto3.client(
                "workspaces", region_name=region
            ).rebuild_workspaces(
                RebuildWorkspaceRequests=[
                    {"WorkspaceId": workspace_id},
                ]
            )
            found = True
            processed_ids.append(workspace_id)
            processed_count += 1
            time.sleep(1)
            if not found:
                print(f"{workspace_id} not found in either region")

        except Exception or ClientError as e:
            print(f"ERROR: {workspace_id} | {e}")

print(f"{processed_count} Workspaces Rebuilt")
print(f"{processed_ids}")
