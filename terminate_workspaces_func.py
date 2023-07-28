import boto3
import time
import csv
from botocore.exceptions import ClientError

# import workspace ids in to a list


def import_csv(filename):
    with open(filename, newline="", encoding="utf-8-sig") as inputfile:
        ws_id = [row[0] for row in csv.reader(inputfile)]
    return ws_id


# check if workspace exist


def gather_workspace(id, client):
    checking_ws = client.describe_workspaces(
        WorkspaceIds=[
            str(id),
        ]
    )
    if len(checking_ws["Workspaces"]):
        return True
    else:
        return False


# terminate workspaces


def terminate_workspaces(id, client):
    print(f"Processing {id}")
    results = client.terminate_workspaces(
        TerminateWorkspaceRequests=[
            {"WorkspaceId": str(id)},
        ]
    )

    return results


# print message if termination fails


def if_failed(term):
    if len(term["FailedRequests"]):
        failed_id = term["FailedRequests"]["WorkspaceId"]
        error_message = term["FailedRequests"]["ErrorMessage"]
        print(f"Failed to term WorkspaceId: {failed_id} | {error_message}")


def main():
    filename = "/Users/jabreu1/Documents/Workspaces/workspace_ids.csv"
    regions = ["us-east-1", "us-west-2", "ap-northeast-1"]
    accounts = ["933881799506", "557431213659", "526793762506"]
    sts_client = boto3.client("sts", region_name="us-east-1")
    termed_count = 0
    processed_ids = []
    workspace_ids = import_csv(filename)
    retry_count = 0

    #loop through the accounts
    for account in accounts:
        assume_role = sts_client.assume_role(
            RoleArn=f"arn:aws:iam::{account}:role/CHEWY-cross-jenkins",
            RoleSessionName="Joel_Abreu_Workspace_Report",
        )
        access_key = assume_role["Credentials"]["AccessKeyId"]
        secret_key = assume_role["Credentials"]["SecretAccessKey"]
        session_token = assume_role["Credentials"]["SessionToken"]
        # loop through ids in list
        for id in workspace_ids:
            found = False
            # loop through regions
            for region in regions:
                # generate client for each region
                client = boto3.client(
                    "workspaces",
                    region_name=region,
                    aws_access_key_id=access_key,
                    aws_secret_access_key=secret_key,
                    aws_session_token=session_token,
                )
                # check if id was already processed
                if id in processed_ids:
                    continue
                workspaces = gather_workspace(id, client)
                try:
                    # if workspace id exist
                    if workspaces:
                        # flag as true
                        found = True
                        # terminate the workspace
                        term = terminate_workspaces(id, client)
                        # if it failed, print it
                        if_failed(term)
                        # add to procesed list
                        processed_ids.append(id)
                        # add to term count
                        termed_count += 1
                # catch error and print them

                except Exception as e:
                    print(f"Exception error {id}| Error: {e}")
            # catch if not found in either region
            if not found:
                print(f"{id} not found in either region")
            # exponential backoff strategy
            retry_count += 1
            time.sleep(2**retry_count)
        # print total amount of termed workspaces
        print(f"Sucessfully terminated {termed_count} Workspaces")


if __name__ == "__main__":
    main()
