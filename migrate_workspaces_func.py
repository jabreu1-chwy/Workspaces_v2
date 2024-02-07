import boto3
import csv
import time

# import from csv


def import_csv(filename):
    with open(filename, newline="", encoding="utf-8-sig") as inputfile:
        workspace_ids = [row[0] for row in csv.reader(inputfile)]
    return workspace_ids


# migrate woorkspaces


def migrate_workspace(client, id, bundle_id):
    response = client.migrate_workspace(SourceWorkspaceId=id, BundleId=bundle_id)
    target = response["TargetWorkspaceId"]
    print(f"New ID: {target}")
    print("|")


def main():
    filename = "/Users/jabreu1/Documents/Workspaces/workspace_ids.csv"
    region = "us-east-1"
    bundle_id = "wsb-w7d4p46ln"
    client = boto3.client("workspaces", region_name=region)

    # import id's into a list
    import_csv(filename)
    ids = import_csv(filename)
    # counter
    processed = 0
    # loop through id's
    for id in ids:
        print(f"Processing {id}")
        try:
            # migrate workspaces
            migrate_workspace(client, id, bundle_id)
            # add to counter
            processed += 1
        except Exception as e:
            print(f"ERROR: {id} | {e}")
        time.sleep(1)
    print(f"{processed} Workspaces migrated")


if __name__ == "__main__":
    main()
