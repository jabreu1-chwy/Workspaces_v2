import boto3
import time
import csv
from botocore.exceptions import ClientError

# import workspace IDs from a CSV file into a list
def import_csv(filename):
    with open(filename, newline="", encoding="utf-8-sig") as inputfile:
        ws_ids = [row[0] for row in csv.reader(inputfile)]
    return ws_ids

# check if a workspace exists
def gather_workspace(id, client):
    checking_ws = client.describe_workspaces(WorkspaceIds=[str(id)])
    return len(checking_ws["Workspaces"]) > 0

# terminate workspaces
def terminate_workspaces(id, client):
    print(f"Terminating {id}")
    results = client.terminate_workspaces(
        TerminateWorkspaceRequests=[{"WorkspaceId": str(id)}]
    )
    return results

# print a message if workspace termination fails
def if_failed(term):
    if len(term["FailedRequests"]):
        failed_id = term["FailedRequests"]["WorkspaceId"]
        error_message = term["FailedRequests"]["ErrorMessage"]
        print(f"Failed to terminate WorkspaceId: {failed_id} | {error_message}")

def main():
    filename = "/Users/jabreu1/Documents/Workspaces/workspace_ids.csv"
    regions = ["us-east-1", "us-west-2", "ap-northeast-1"]
    accounts = ["557431213659"]
    # "526793762506", "933881799506"
    sts_client = boto3.client("sts", region_name="us-east-1")
    termed_count = 0
    processed_ids = set()
    workspace_ids = import_csv(filename)
    retry_count = 0

    # Loop through the accounts
    for account in accounts:
        assume_role = sts_client.assume_role(
            RoleArn=f"arn:aws:iam::{account}:role/CHEWY-cross-jenkins",
            RoleSessionName="Joel_Abreu_Monthly_Cleanup",
        )
        access_key = assume_role["Credentials"]["AccessKeyId"]
        secret_key = assume_role["Credentials"]["SecretAccessKey"]
        session_token = assume_role["Credentials"]["SessionToken"]

        # Loop through the workspace IDs in the list
        for ws_id in workspace_ids:
            # Check if the ID was already processed
            if ws_id in processed_ids:
                continue

            found = False

            # Loop through the regions
            for region in regions:
                # Generate a client for each region
                client = boto3.client(
                    "workspaces",
                    region_name=region,
                    aws_access_key_id=access_key,
                    aws_secret_access_key=secret_key,
                    aws_session_token=session_token,
                )

                # Check if the workspace ID exists
                workspace_exists = gather_workspace(ws_id, client)

                try:
                    # If workspace ws_id exists, terminate the workspace
                    if workspace_exists:
                        found = True
                        termination_result = terminate_workspaces(ws_id, client)
                        # If termination fails, print an error message
                        if_failed(termination_result)
                        processed_ids.add(ws_id)  # Add to processed list
                        termed_count += 1  # Increase termination count
                    # if it doesnt, continue to next ws_id  
                    else:
                        continue

                # Catch and print any exceptions during termination
                except Exception as e:
                    print(f"Exception error {ws_id} | Error: {e}")

            # If the workspace ID was not found in any region
            if not found:
                print(f"{ws_id} not found in {account}")

            # Exponential backoff strategy before processing the next workspace
            retry_count += 1
            time.sleep(1 ** retry_count)

    # Print the total number of terminated workspaces
    print(f"Successfully terminated {termed_count} Workspaces")


if __name__ == "__main__":
    main()
