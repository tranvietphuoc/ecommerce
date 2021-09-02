from tests import client


client = client()


def test_empty_db(client):
    """start with a blank database"""

    rv = client.get("/")
    assert b"No entries here so far" in rv.data
