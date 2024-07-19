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


def restore(client, ids):
    for id in ids:
        print(f"Restoring {id}...")
        response = client.restore_workspaces(
            RebuildWorkspaceRequests=[
                {"WorkspaceId": id},
            ]
        )
        return response




def main():
    client = boto3.client("workspaces", region_name="us-west-2")
    ids = get_workspaces(client)
    if ids:
        restore(client, ids)
    else:
        print("No UNHEALTHY workspaces found.")


if __name__ == "__main__":
    main()
