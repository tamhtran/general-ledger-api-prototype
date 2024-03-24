def test_account_get_all(test_app_with_db):
    response = test_app_with_db.get("/account/")
    print(response)
    assert response.status_code == 200


def test_account_get_by_id(test_app_with_db):
    response = test_app_with_db.get("/account/10")
    assert response.status_code == 200


def test_account_get_by_id_invalid(test_app_with_db):
    response = test_app_with_db.get("/account/10000")
    assert response.status_code == 404
    assert response.json()["detail"] == "Account not found"