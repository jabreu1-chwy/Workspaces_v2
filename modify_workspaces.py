import boto3
import csv
import time

# imports list of workspace id's and adds to list


def import_csv(filename):
    with open(filename, newline="", encoding="utf-8-sig") as inputfile:
        workspace_ids = [row[0] for row in csv.reader(inputfile)]
    return workspace_ids


# check if workspace exist


def gather_workspace(id, client):
    retry_count = 0
    retry_count += 1
    time.sleep(1**retry_count)
    checking_ws = client.describe_workspaces(
        WorkspaceIds=[
            str(id),
        ]
    )
    if len(checking_ws["Workspaces"]):
        return True
    else:
        return False


# # modify the workspace properties


def modify_ws(client, id):
    client.modify_workspace_properties(
        WorkspaceId=id,
        WorkspaceProperties={
            "RunningMode": "ALWAYS_ON",
            # "RunningModeAutoStopTimeoutInMinutes": 120,
        },
    )
    print(f"{id} Modified")


def main():
    filename = "/Users/jabreu1/Documents/Workspaces/workspace_ids.csv"
    regions = ["us-east-1", "us-west-2", "ap-northeast-1"]
    sts_client = boto3.client("sts", region_name="us-east-1")
    accounts = ["933881799506"]
    processed_ids = []
    ids = import_csv(filename)

    for account in accounts:
        assume_role = sts_client.assume_role(
            RoleArn=f"arn:aws:iam::{account}:role/CHEWY-cross-jenkins",
            RoleSessionName="Joel_Abreu_Workspace_Report",
        )
        access_key = assume_role["Credentials"]["AccessKeyId"]
        secret_key = assume_role["Credentials"]["SecretAccessKey"]
        session_token = assume_role["Credentials"]["SessionToken"]
        # loops through the ids
        for id in ids:
            found = False
            if id in processed_ids:
                continue
            # loop through regions
            for region in regions:
                client = boto3.client(
                    "workspaces",
                    region_name=region,
                    aws_access_key_id=access_key,
                    aws_secret_access_key=secret_key,
                    aws_session_token=session_token,
                )
                # gather workspace info
                workspaces = gather_workspace(id, client)
                # if it exist
                if workspaces:
                    found = True
                    # check if it was already processed
                    if id not in processed_ids:
                        try:
                            # modify the workspace
                            modify_ws(client, id)
                            processed_ids.append(id)
                        # catch error
                        except Exception as e:
                            print(f"ERROR: {id} | {e}")
            if not found:
                print(f"{id} not found in either region | {account}")
    print(f"{len(processed_ids)} completed")


if __name__ == "__main__":
    main()
