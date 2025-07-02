import pytest
from main import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Smart CGPA Calculator" in response.data

def test_ug_year_flow(client):
    response = client.post("/", data={"program": "UG", "mode": "year"}, follow_redirects=True)
    assert b"Year 1 marks" in response.data

def test_pg_sem_flow(client):
    response = client.post("/", data={"program": "PG", "mode": "semester"}, follow_redirects=True)
    assert b"Semester 1 marks" in response.data

def test_calculation_logic(client):
    response = client.post("/marks?program=UG&mode=year", data={
        "total_1": "100", "obtained_1": "80",
        "total_2": "100", "obtained_2": "90",
        "total_3": "100", "obtained_3": "100",
    })
    assert response.status_code == 200
    assert b"Your CGPA is:" in response.data

def test_edge_case_zero_total(client):
    response = client.post("/marks?program=UG&mode=year", data={
        "total_1": "0", "obtained_1": "0",
        "total_2": "100", "obtained_2": "50",
        "total_3": "100", "obtained_3": "60",
    })
    assert response.status_code == 200
    assert b"Your CGPA is:" in response.data
