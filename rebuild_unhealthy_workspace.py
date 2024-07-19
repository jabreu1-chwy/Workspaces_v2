import boto3


def paginate(method, **kwargs):
    client = method.__self__
    paginator = client.get_paginator(method.__name__)
    for page in paginator.paginate(**kwargs).result_key_iters():
        for result in page:
            yield result


def get_workspaces(client):
    ids = []
    for workspace in paginate(client.describe_workspaces):
        state = workspace["State"]
        if state == "UNHEALTHY":
            ids.append(workspace["WorkspaceId"])
    return ids


def rebuild(client, ids):
    for id in ids:
        print(f"Rebuilding {id}...")
        response = client.rebuild_workspaces(
            RebuildWorkspaceRequests=[
                {"WorkspaceId": id},
            ]
        )
        if len(response["FailedRequests"]):
            ws_id = response["FailedRequests"][0]["WorkspaceId"]
            error = response["FailedRequests"][0]["ErrorMessage"]
            print(f"Rebuild failed for {ws_id} | {error}")




def main():
    client = boto3.client("workspaces", region_name="us-east-1")

    ids = get_workspaces(client)
    if ids:
        rebuild(client, ids)
    else:
        print("No UNHEALTHY workspaces found.")


if __name__ == "__main__":
    main()
