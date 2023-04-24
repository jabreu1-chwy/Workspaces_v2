import datetime
import describe_workspaces_func
import terminate_workspaces_func


def test_get_last_login_no_status():
    status = {
        "WorkspacesConnectionStatus": []
    }

    time_difference_days, last_known_user_login = describe_workspaces_func.get_last_login(
        status)
    assert last_known_user_login == "No login registered"
    assert time_difference_days == "N/A"


def test_get_last_login_no_timestamp():
    status = {
        "WorkspacesConnectionStatus": [{
            "fake_data": True
        }]
    }
    time_difference_days, last_known_user_login = describe_workspaces_func.get_last_login(
        status)
    assert last_known_user_login == "No login registered"
    assert time_difference_days == "N/A"


def test_get_last_login_timestamp():
    status = {
        "WorkspacesConnectionStatus": [{
            "LastKnownUserConnectionTimestamp": "2023-02-21 20:18:51.079000-05:00"
        }]
    }
    dt = datetime.datetime.strptime(
        status["WorkspacesConnectionStatus"][0]['LastKnownUserConnectionTimestamp'], "%Y-%m-%d %H:%M:%S.%f%z"
    )
    time_difference_days, last_known_user_login = describe_workspaces_func.get_last_login(
        status)
    assert last_known_user_login == dt
    assert time_difference_days > 30


def test_import_csv(mocker):
    mocker.patch("builtins.open", mocker.mock_open(read_data="ws-gb7f917p0"))
    content = terminate_workspaces_func.import_csv("nuclearsecrets.txt")
    assert content == ["ws-gb7f917p0"]
