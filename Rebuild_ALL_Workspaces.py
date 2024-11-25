import boto3
import time
from botocore.exceptions import ClientError

regions = ["us-east-1", "us-west-2"]

def get_all_workspaces(client):
    paginator = client.get_paginator("describe_workspaces")
    workspaces = []
    
    for page in paginator.paginate():
        workspaces.extend(page["Workspaces"])
    
    return workspaces


def rebuild_workspace(client, workspace_id):
    try:
        client.rebuild_workspaces(
            RebuildWorkspaceRequests=[{"WorkspaceId": workspace_id}]
        )
        print(f"Rebuilding {workspace_id}")
        return True
    except (Exception, ClientError) as e:
        print(f"ERROR rebuilding {workspace_id}: {e}")
        return False


def process_region(region):
    client = boto3.client("workspaces", region_name=region)
    workspaces = get_all_workspaces(client)
    processed_ids = []
    processed_count = 0

    for workspace in workspaces:
        workspace_id = workspace["WorkspaceId"]
        if rebuild_workspace(client, workspace_id):
            processed_ids.append(workspace_id)
            processed_count += 1
            time.sleep(1)

    print(f"Region: {region} | {processed_count} Workspaces Rebuilt")
    return processed_ids


def rebuild_all_workspaces():
    all_processed_ids = []

    for region in regions:
        try:
            processed_ids = process_region(region)
            all_processed_ids.extend(processed_ids)
        except (Exception, ClientError) as e:
            print(f"ERROR retrieving Workspaces in region {region}: {e}")

    print(f"Total Workspaces Rebuilt: {len(all_processed_ids)}")


rebuild_all_workspaces()
