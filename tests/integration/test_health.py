def test_health(fix_client):
    res = fix_client.get("/health")
    assert res.json()["status"] == "success"
