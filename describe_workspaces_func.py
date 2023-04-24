import boto3
import os
import csv
import datetime
import json


def paginate(method, **kwargs):
    client = method.__self__
    paginator = client.get_paginator(method.__name__)
    for page in paginator.paginate(**kwargs).result_key_iters():
        for result in page:
            yield result


# open/create csv and writes the header info


def create_write_row(writer):
    # Open a CSV file for writing in the specified directory
    # with open(os.path.join(directory, filename), "w", newline="") as file:
    header_row = [
        "WorkspaceId",
        "UserName",
        "BundleId",
        "IpAddress",
        "ComputerName",
        "State",
        "RunningMode",
        "TimeoutInMinutes",
        "Region",
        "LastConnectionTime",
        "DaysSinceLastLogin",
    ]

    # creates header row in the CSV file
    writer.writerow(header_row)


# gather workspace connection info


def get_connection_status(client, id):
    connection_status = client.describe_workspaces_connection_status(WorkspaceIds=[
                                                                     id])
    # print(json.dumps(connection_status, default=str, indent=4))
    return connection_status


# gather workspace timestamps


def get_last_login(status):
    LastKnownUserLogin = "No login registered"
    time_difference_days = "N/A"
    try:
        if len(status["WorkspacesConnectionStatus"]):
            if (
                "LastKnownUserConnectionTimestamp"
                in status["WorkspacesConnectionStatus"][0]
            ):
                # convert to str
                LastKnownUserConnectionTimestamp = str(
                    status["WorkspacesConnectionStatus"][0][
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
                    time_difference.total_seconds() // 86400)

    except ValueError:
        LastKnownUserLogin = "Invalid timestamp format"
        time_difference_days = " "
    # print(time_difference, time_difference_days)
    return time_difference_days, LastKnownUserLogin


# export results to a csv


def write_workspace_to_csv(
    writer, workspace, region, last_known_user_login, time_difference_days
):
    writer.writerow(
        [
            workspace["WorkspaceId"],
            workspace["UserName"],
            workspace["BundleId"],
            workspace.get("IpAddress", "No IP address"),
            workspace.get("ComputerName", "Null"),
            workspace["State"],
            workspace["WorkspaceProperties"]["RunningMode"],
            workspace["WorkspaceProperties"].get(
                "RunningModeAutoStopTimeoutInMinutes", "Null"
            ),
            region,
            last_known_user_login,
            time_difference_days,
        ]
    )


def main():
    regions = ["us-east-1", "us-west-2"]
    filename = input("Enter the filename: ")
    directory = input("Enter the file path you like this exported to: ")

    # opens csv and writes the headers
    with open(os.path.join(directory, filename), "w", newline="") as file:
        writer = csv.writer(file)

        create_write_row(writer)
        # loop through regions
        for region in regions:
            # generate client
            client = boto3.client("workspaces", region_name=region)

            # gather workspaces
            for workspace in paginate(client.describe_workspaces):
                # variable for the workspace id
                id = workspace["WorkspaceId"]
                status = get_connection_status(client, id)
                print(f"Processing {id}")
                # calculate last known user login and time difference
                time_difference_days, last_known_user_login = get_last_login(
                    status)

                try:
                    # write info to csv file
                    write_workspace_to_csv(
                        writer,
                        workspace,
                        region,
                        last_known_user_login,
                        time_difference_days,
                    )
                except Exception as e:
                    print(f"Error with {id} | {e}")


if __name__ == "__main__":
    main()
