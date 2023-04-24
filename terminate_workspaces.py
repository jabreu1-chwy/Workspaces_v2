import boto3
import time
import csv
from botocore.exceptions import ClientError


regions = ["us-east-1", "us-west-2"]

term_list = []
termed_count = 0
processed_ids = []

header_skipped = False
with open(
    "/Users/jabreu1/Documents/Workspaces/terminate_workspaces.csv",
    newline="",
    encoding="utf-8-sig",
) as inputfile:
    for row in csv.reader(inputfile):
        if not header_skipped:
            header_skipped = True
            continue
        term_list.append(row[0])
print(term_list)


for region in regions:
    workspaces = boto3.client("workspaces", region_name=region)
    for entry in term_list:
        if entry in processed_ids:
            continue
        try:
            # checks if it exist first
            checking_ws = workspaces.describe_workspaces(WorkspaceIds=[entry])
            if not checking_ws["Workspaces"]:
                continue

            # terminate the workspace
            response = workspaces.terminate_workspaces(
                TerminateWorkspaceRequests=[
                    {"WorkspaceId": str(entry)},
                ]
            )
            # print message if failed
            if not len(response["FailedRequests"]) == 0:
                print(
                    f"Failed to terminate WorkspaceId: {response['FailedRequests']['WorkspaceId']} | {response['FailedRequests']['ErrorMessage']} {region}"
                )
                time.sleep(2)
            else:
                print(f"Successfully terminated WorkspaceId: {entry}")
                termed_count += 1
                processed_ids.append(entry)
        except ClientError as e:
            print(
                f"Term Error for WorkspaceId: {entry} in region {region}: | Error: {e}"
            )
        except Exception as e:
            print(f"Term error with {entry} in region {region}| Error: {e}")

print(f"Sucessfully terminated {termed_count} Workspaces")
