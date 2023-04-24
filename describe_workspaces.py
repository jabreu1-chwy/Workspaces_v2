import boto3
import csv
import time
import datetime
import os


regions = ["us-east-1", "us-west-2"]
filename = input("Enter the filename: ")
directory = input("Enter the file path you like this exported to: ")


def paginate(method, **kwargs):
    client = method.__self__
    paginator = client.get_paginator(method.__name__)
    for page in paginator.paginate(**kwargs).result_key_iters():
        for result in page:
            yield result


# Open a CSV file for writing in the specified directory
with open(os.path.join(directory, filename), "w", newline="") as file:
    writer = csv.writer(file)

    # Write the header row to the CSV file
    writer.writerow(
        [
            "WorkspaceId",
            "UserName",
            "BundleId",
            "IpAddress",
            "ComputerName",
            "State",
            "RunningMode",
            "AutoStopTimeout",
            "Region",
            "LastConnectionTime",
            "DaysSinceLastLogin",
        ]
    )

    for region in regions:
        client = boto3.client("workspaces", region_name=region)

        for workspace in paginate(client.describe_workspaces):
            try:
                conection_status = client.describe_workspaces_connection_status(
                    WorkspaceIds=[workspace["WorkspaceId"]]
                )
                print(f"Processing {workspace['WorkspaceId']}")

                if len(conection_status["WorkspacesConnectionStatus"]):
                    if (
                        "LastKnownUserConnectionTimestamp"
                        in conection_status["WorkspacesConnectionStatus"][0]
                    ):

                        # convert to str
                        LastKnownUserConnectionTimestamp = str(
                            conection_status["WorkspacesConnectionStatus"][0][
                                "LastKnownUserConnectionTimestamp"
                            ]
                        )

                        # format time/date
                        LastKnownUserLogin = datetime.datetime.strptime(
                            LastKnownUserConnectionTimestamp, "%Y-%m-%d %H:%M:%S.%f%z"
                        )
                        # current date
                        current_date = datetime.datetime.now(datetime.timezone.utc)
                        # time difference
                        time_difference = current_date - LastKnownUserLogin
                        # round down to days
                        time_difference_days = int(
                            time_difference.total_seconds() // 86400
                        )
                    else:
                        LastKnownUserLogin = "No login registered"
                        time_difference_days = " "
                else:
                    continue
                # write the workspace data as a row in the CSV file
                writer.writerow(
                    [
                        workspace["WorkspaceId"],
                        workspace["UserName"],
                        workspace["BundleId"],
                        workspace.get("IpAddress", "No IP address"),
                        workspace.get("ComputerName", "Null"),
                        workspace["State"],
                        workspace["WorkspaceProperties"]["RunningMode"],
                        workspace["WorkspaceProperties"][
                            "RunningModeAutoStopTimeoutInMinutes"
                        ],
                        region,
                        LastKnownUserLogin,
                        time_difference_days,
                    ]
                )
            except Exception as e:
                print(f"{workspace['WorkspaceId']} | {e}")
                time.sleep(1)
