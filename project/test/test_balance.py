def test_balance_before_transactions(test_app_with_db):
    response = test_app_with_db.get("/balance/10/2021-02-02")
    assert response.status_code == 201


def test_balance_invalid_date(test_app_with_db):
    response = test_app_with_db.get("/balance/10/q5")
    assert response.status_code == 403
    assert response.json()["detail"] == "Date not valid"


def test_balance_invalid_account(test_app_with_db):
    response = test_app_with_db.get("/balance/1000000/2021-02-02")
    assert response.status_code == 404
    assert response.json()["detail"] == "Account not found"


def test_balance_invalid_region(test_app_with_db):
    response = test_app_with_db.get("/balance/10/2021-02-02?region_id=1000000")
    assert response.status_code == 405
    assert response.json()["detail"] == "Region not found"


def test_balance_invalid_balance(test_app_with_db):
    response = test_app_with_db.get("/balance/10/2019-01-01")
    assert response.status_code == 406
    assert response.json()["detail"] == "Balance not found"


def test_balance_simple(test_app_with_db):
    response = test_app_with_db.get("/balance/10/2022-01-01")
    assert response.status_code == 201

    expected_balance = -100-5000+300+400+100
    response_dict = response.json()
    assert response_dict["balance"] == expected_balance


def test_balance_zero(test_app_with_db):
    response = test_app_with_db.get("/balance/10/2021-02-02")
    assert response.status_code == 201

    expected_balance = 0
    response_dict = response.json()
    assert response_dict["balance"] == expected_balance


def test_balance_with_region(test_app_with_db):
    response = test_app_with_db.get("/balance/10/2021-07-03?region_id=3")
    assert response.status_code == 201

    expected_balance = 400
    response_dict = response.json()
    assert response_dict["balance"] == expected_balance


def test_balance_simple(test_app_with_db):
    response = test_app_with_db.get("/balance/10/2022-01-01")
    assert response.status_code == 201

    expected_balance = -100-5000+300+400+100
    response_dict = response.json()
    assert response_dict["balance"] == expected_balance

def test_balance_with_region(test_app_with_db):
    response = test_app_with_db.get("/balance/10/2021-07-03?region_id=2")
    assert response.status_code == 201

    expected_balance = 400
    response_dict = response.json()
    assert response_dict["balance"] == expected_balance

