"""Slice 1: sign-in and the my groups list. Each test names the criterion it proves."""
from tests.conftest import sign_in


def test_ac12_groups_page_without_session_redirects_to_login(client):
    response = client.get("/groups")
    assert response.status_code == 302
    assert response.headers["location"] == "/login"


def test_ac12_groups_api_without_session_returns_401(client):
    response = client.get("/api/groups")
    assert response.status_code == 401
    assert response.json() == {"error": "Sign in first"}


def test_ac13_signed_in_user_sees_only_her_groups_with_role(client):
    assert sign_in(client).status_code == 200
    groups = client.get("/api/groups").json()["groups"]
    assert [(g["name"], g["role"]) for g in groups] == [
        ("Flat on Vitosha Blvd", "owner"),
        ("Weekend in Plovdiv", "member"),
    ]
    assert "Rila Monastery trip" not in [g["name"] for g in groups]
    assert client.get("/groups").status_code == 200


def test_ac14_wrong_password_is_refused_and_creates_no_session(client, store):
    response = sign_in(client, password="wrong")
    assert response.status_code == 401
    assert response.json() == {"error": "Wrong e-mail or password"}
    assert store.sessions == {}


def test_ac15_removed_membership_disappears_from_the_list(client, store):
    sign_in(client)
    del store.memberships[(1, 2)]
    names = [g["name"] for g in client.get("/api/groups").json()["groups"]]
    assert names == ["Flat on Vitosha Blvd"]


def test_ac16_sign_out_deletes_the_session(client, store):
    sign_in(client)
    assert len(store.sessions) == 1
    client.post("/api/auth/logout")
    assert store.sessions == {}
    assert client.get("/groups").headers["location"] == "/login"
