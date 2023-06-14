import boto3
import csv

# imports list of workspace id's and adds to list


def import_csv(filename):
    with open(filename, newline="", encoding="utf-8-sig") as inputfile:
        workspace_ids = [row[0] for row in csv.reader(inputfile)]
    return workspace_ids


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


# # modify the workspace properties


def modify_ws(client, id):
    client.modify_workspace_properties(
        WorkspaceId=id,
        WorkspaceProperties={
            "RunningMode": "ALWAYS_ON",
            # "RunningModeAutoStopTimeoutInMinutes": 60,
        },
    )
    print(f"Modifying {id}...")

def main():
    filename = "./workspace_ids.csv"
    regions = ["us-east-1", "us-west-2"]
    processed_ids = []
    ids = import_csv(filename)
    # loops through the ids
    for id in ids:
        found = False
        # loop through regions
        for region in regions:
            client = boto3.client("workspaces", region_name=region)
            # gather workspace info
            workspaces = gather_workspace(id, client)
            # if it exist
            if workspaces == True:
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
            print(f"{id} not found in either region")
    print(f"{len(processed_ids)} modified")


if __name__ == "__main__":
    main()
