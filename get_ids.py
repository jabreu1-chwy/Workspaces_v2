import boto3
import csv


def import_csv(filename):
    with open(filename, newline="", encoding="utf-8-sig") as inputfile:
        user_ids = [row[0] for row in csv.reader(inputfile)]
    return user_ids


def get_workspace(client, usernames):
    list = []
    try:
        for username in usernames:
            ws = client.describe_workspaces(
                DirectoryId="d-9067b2fb26", UserName=username
            )
            list.append(ws["Workspaces"][0]["WorkspaceId"])
    except Exception as e:
        print(f"{username} | {e}")
    return list


def modify(client, ws_ids):
    for id in ws_ids:
        print(f"modifying {id}")
        try:
            response = client.modify_workspace_properties(
                WorkspaceId=id, WorkspaceProperties={"ComputeTypeName": "POWERPRO"}
            )
        except Exception as e:
            print(f"{id} | {e}")
    print("Job Complete.")
    return response


def main():
    client = boto3.client("workspaces")
    filename = "/Users/jabreu1/Documents/Workspaces/workspace_ids.csv"

    usernames = import_csv(filename)
    ws_ids = get_workspace(client, usernames)
    modify(client, ws_ids)


main()
