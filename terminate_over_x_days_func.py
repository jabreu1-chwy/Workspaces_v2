import datetime
import time
import boto3


def paginate(method, **kwargs):
    client = method.__self__
    paginator = client.get_paginator(method.__name__)
    for page in paginator.paginate(**kwargs).result_key_iters():
        for result in page:
            yield result


def get_workspace_status(id, client):
    connection_status = client.describe_workspaces_connection_status(WorkspaceIds=[id])
    return connection_status


def get_last_login(status):
    timestamp = str(
        status["WorkspacesConnectionStatus"][0]["LastKnownUserConnectionTimestamp"]
    )
    # format time/date
    LastKnownUserLogin = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f%z")
    # current date
    current_date = datetime.datetime.now(datetime.timezone.utc)
    # time difference
    time_difference = current_date - LastKnownUserLogin
    # round down to days
    time_difference_days = int(time_difference.total_seconds() // 86400)
    return time_difference_days


def terminate_workspace(client, id):
    resp = client.terminate_workspaces(TerminateWorkspaceRequests=[id])
    return resp


def should_be_terminated(status):
    term = False
    # if no data, should not term
    if not len(status["WorkspacesConnectionStatus"]):
        term = False
    elif "timestamp" in status["WorkspacesConnectionStatus"][0]:
        time_difference_days = get_last_login(status)
        if time_difference_days > 90:
            term = True
    else:
        # this has a status and no last login date - we should term
        term = True

    # if we got here with no status, return the default no matter what
    return term


def main():
    termed_workspaces = 0
    regions = ["us-east-1", "us-west-2"]

    for region in regions:
        # generate a client for each region
        client = boto3.client("workspaces", region_name=region)
        # paginate through each workspace in that region
        for workspace in paginate(client.describe_workspaces):
            id = workspace["WorkspaceId"]
            print(f"Processing {id}")

            # get some details around each workspace
            status = get_workspace_status(id, client)

            # see if we should term or not
            term = should_be_terminated(status)
            if term:
                try:
                    terminate_workspace(client, id)

                except Exception as e:
                    print(f"Error terminating workspace {id} | {e}")
                    time.sleep(1)

    print(f"Successfully terminated {termed_workspaces} Workspaces")
