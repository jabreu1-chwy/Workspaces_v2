import boto3
import json

client = boto3.client("workspaces")
response = client.describe_workspace_directories(
    DirectoryIds=[
        "d-90677397c8",
    ]
)

print(json.dumps(response, default=str, indent=4))


# {
#     "Directories": [
#         {
#             "DirectoryId": "d-90677397c8",
#             "Alias": "chewy-workspaces",
#             "DirectoryName": "chewy.local",
#             "RegistrationCode": "SLiad+5BTRW2",
#             "SubnetIds": [
#                 "subnet-0155176930d1f3e62",
#                 "subnet-090ee012cb1af1d02"
#             ],
#             "DnsIpAddresses": [
#                 "10.1.103.20",
#                 "10.2.103.20"
#             ],
#             "CustomerUserName": "Administrator",
#             "IamRoleId": "arn:aws:iam::933881799506:role/workspaces_DefaultRole",
#             "DirectoryType": "AD_CONNECTOR",
#             "WorkspaceSecurityGroupId": "sg-082937262db3d1913",
#             "State": "REGISTERED",
#             "WorkspaceCreationProperties": {
#                 "EnableWorkDocs": false,
#                 "EnableInternetAccess": false,
#                 "DefaultOu": "OU=WorkSpaces,OU=Computers,OU=Chewy,DC=chewy,DC=local",
#                 "UserEnabledAsLocalAdministrator": false,
#                 "EnableMaintenanceMode": true
#             },
#             "WorkspaceAccessProperties": {
#                 "DeviceTypeWindows": "ALLOW",
#                 "DeviceTypeOsx": "ALLOW",
#                 "DeviceTypeWeb": "ALLOW",
#                 "DeviceTypeIos": "DENY",
#                 "DeviceTypeAndroid": "DENY",
#                 "DeviceTypeChromeOs": "ALLOW",
#                 "DeviceTypeZeroClient": "ALLOW",
#                 "DeviceTypeLinux": "ALLOW"
#             },
#             "Tenancy": "SHARED",
#             "SelfservicePermissions": {
#                 "RestartWorkspace": "ENABLED",
#                 "IncreaseVolumeSize": "DISABLED",
#                 "ChangeComputeType": "DISABLED",
#                 "SwitchRunningMode": "DISABLED",
#                 "RebuildWorkspace": "DISABLED"
#             },
#             "SamlProperties": {
#                 "Status": "DISABLED",
#                 "UserAccessUrl": "",
#                 "RelayStateParameterName": "RelayState"
#             }
#         }
#     ],
#     "ResponseMetadata": {
#         "RequestId": "aaddc37b-46f1-47b6-bea4-905e9aa0ae82",
#         "HTTPStatusCode": 200,
#         "HTTPHeaders": {
#             "x-amzn-requestid": "aaddc37b-46f1-47b6-bea4-905e9aa0ae82",
#             "content-type": "application/x-amz-json-1.1",
#             "content-length": "1313",
#             "date": "Mon, 09 Jan 2023 21:16:53 GMT"
#         },
#         "RetryAttempts": 0
#     }
# }
