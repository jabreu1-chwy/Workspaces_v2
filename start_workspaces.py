import boto3
import csv

regions = ["us-east-1", "us-west-2"]
processed_ids = []

with open(
    "/Users/jabreu1/Library/CloudStorage/OneDrive-Chewy.com,LLC/Documents/Workspaces/start_workspaces.csv",
    newline="",
    encoding="utf-8-sig",
) as inputfile:
    workspace_ids = [row[0] for row in csv.reader(inputfile)]

for workspace_id in workspace_ids:
    found = False

    for region in regions:
        if workspace_id in processed_ids:
            continue

        try:
            # checks if it exists first
            checking_ws = boto3.client(
                "workspaces", region_name=region
            ).describe_workspaces(WorkspaceIds=[workspace_id])
            if not checking_ws["Workspaces"]:
                continue

            # if checking_ws["Workspaces"][0]["State"] == "AVAILABLE":
            #     # print(f"{workspace_id} is already available in {region}")
            #     found = True
            #     # processed_ids.append(workspace_id)
            #     # break

            modify_ws = boto3.client(
                "workspaces", region_name=region
            ).modify_workspace_properties(
                WorkspaceId=workspace_id,
                WorkspaceProperties={
                    "RunningMode": "AUTO_STOP",
                    "RunningModeAutoStopTimeoutInMinutes": 60,
                },
            )
            print(f"Processed {workspace_id} in {region}")
            processed_ids.append(workspace_id)
            found = True
            # break

            # start_ws = boto3.client("workspaces", region_name=region).start_workspaces(
            #     StartWorkspaceRequests=[
            #         {"WorkspaceId": workspace_id},
            #     ]
            # )

            # if len(start_ws["FailedRequests"]) > 0:
            #     print(
            #         f"Failed to start {workspace_id} in {region}: {start_ws['FailedRequests'][0]['ErrorMessage']}"
            #     )
            # else:
            #     print(f"Processed {workspace_id} in {region}")
            #     processed_ids.append(workspace_id)
            #     found = True
            #     break

        except Exception as e:
            print(f"{workspace_id} in {region} | {e}")

    if not found:
        print(f"{workspace_id} not found in either region")
