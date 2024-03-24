def test_region_get_all(test_app_with_db):
    response = test_app_with_db.get("/region/")
    assert response.status_code == 200


def test_region_get_by_id(test_app_with_db):
    response = test_app_with_db.get("/region/1")
    assert response.status_code == 200


def test_region_get_by_id_invalid(test_app_with_db):
    response = test_app_with_db.get("/region/10000")
    assert response.status_code == 404
    assert response.json()["detail"] == "Region not found"