import boto3
import csv
from botocore.exceptions import ClientError
import time

# import usernames from csv into a list


def import_csv(filename):
    with open(filename, newline="", encoding="utf-8-sig") as inputfile:
        usernames = [row[0] for row in csv.reader(inputfile)]
    return usernames


# create workspace, change fields as needed


def create_workspace(username, directoryid, bundleid, client):
    create_ws = client.create_workspaces(
        Workspaces=[
            {
                "DirectoryId": directoryid,
                "UserName": username,
                "BundleId": bundleid,
                "VolumeEncryptionKey": "alias/aws/workspaces",
                "UserVolumeEncryptionEnabled": True,
                "RootVolumeEncryptionEnabled": True,
                "WorkspaceProperties": {
                    "RunningMode": "AUTO_STOP",
                    "RunningModeAutoStopTimeoutInMinutes": 60,
                },
                # "Tags": [
                #     {"Key": "string", "Value": "string"},
                # ],
            },
        ]
    )
    return create_ws


# adds succeful or failed creations to a list to keep track


def add_to_list(results, username, failed_workspaces, created_workspaces):
    if len(results["FailedRequests"]):
        failed_workspaces.append(username)
    elif len(results["PendingRequests"]):
        created_workspaces.append(username)


def print_results(created_workspaces, failed_workspaces):
    if len(created_workspaces):
        print(
            f"Sucessfully created {len(created_workspaces)} Workspaces: {created_workspaces}"
        )
    elif len(failed_workspaces):
        print(
            f"Failed to create {len(failed_workspaces)} Workspaces: {failed_workspaces}"
        )


def main():
    filename = "/Users/jabreu1/Documents/Workspaces/workspace_ids.csv"
    directoryid = "d-9067b2fb26"
    bundleid = "wsb-8xjqdxm7t"
    client = boto3.client("workspaces", region_name="us-east-1")
    created_workspaces = []
    failed_workspaces = []
    usernames = import_csv(filename)
    # loop through all usernames
    for username in usernames:
        try:
            # create workspace
            results = create_workspace(username, directoryid, bundleid, client)
            # adds to list
            add_to_list(results, username, failed_workspaces, created_workspaces)
        except ClientError as e:
            print(f"Client Error for {username}: {e}")
            failed_workspaces.append(username)
        except Exception as e:
            print(f"Exception Error for {username}: {e}")
            failed_workspaces.append(username)
        # 2 second pause between calls
        time.sleep(2)
    print_results(created_workspaces, failed_workspaces)


if __name__ == "__main__":
    main()
