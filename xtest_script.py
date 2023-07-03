import boto3
from botocore.exceptions import ClientError
import json
import time
import csv


# def import_csv(filename):
#     with open(filename, newline="", encoding="utf-8-sig") as inputfile:
#         ws_id = [row[0] for row in csv.reader(inputfile)]
#     return ws_id


def describe(client, id):
    response = client.describe_workspaces(WorkspaceIds=[id])
    return response


def main():
    # filename = "/Users/jabreu1/Documents/Workspaces/workspace_ids.csv"
    # ws_ids = import_csv(filename)'
    id = "ws-6sygyhg56"
    client = boto3.client("workspaces", region_name="us-east-1")
    wsinfo = describe(client, id)
    print(json.dumps(wsinfo, default=str, indent=4))


main()
