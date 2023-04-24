import boto3
import csv

# import from csv


def import_csv(filename):
    with open(filename, newline="", encoding="utf-8-sig") as inputfile:
        workspace_ids = [row[0] for row in csv.reader(inputfile)]
    return workspace_ids


# gather all workspace info


def gather_workspace(id, client):
    checking_ws = client.describe_workspaces(
        WorkspaceIds=[
            str(id),
        ]
    )
    if len(checking_ws["Workspaces"]):
        return checking_ws
    else:
        return False


# check if available


def check_if_available(workspace_info, id, region, processed_ids):
    for workspace in workspace_info["Workspaces"]:
        if workspace["State"] == "AVAILABLE" and workspace["WorkspaceId"] == id:
            print(f"{id} is already available in {region}")
            processed_ids.append(id)
            return True
        else:
            return False


# start workspaces


def start_workspaces(id, client):
    client.start_workspaces(
        StartWorkspaceRequests=[
            {"WorkspaceId": id},
        ]
    )


def main():
    filename = input("Enter the file path and name of file: ")
    regions = ["us-east-1", "us-west-2"]
    processed_ids = []
    ids = import_csv(filename)

    for id in ids:
        found = False
        # loop through regions
        for region in regions:
            # generate client for each region
            client = boto3.client("workspaces", region_name=region)
            workspace_info = gather_workspace(id, client)
            # loop through each id
            if id in processed_ids:
                continue

            try:
                if not workspace_info:
                    continue
                # check if workspace is already running
                check_if_available(workspace_info, id, region, processed_ids)
                # if found start it
                if not check_if_available:
                    start_workspaces(id, client)
            except Exception as e:
                print(f"ERROR: {id} | {e}")
        if not found:
            print(f"{id} not found in either region")
