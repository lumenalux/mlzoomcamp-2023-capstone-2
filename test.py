import requests

def test_model(url, endpoint, data):
    response = requests.post(f"{url}/predict/{endpoint}", json=data)
    print(f"Response from {endpoint}: {response.json()}")


if __name__ == '__main__':
  URL = "http://localhost:5000"

  data = {
      'Pclass': 1.0,
      'Sex': 1.0,
      'Age': 36.0,
      'SibSp': 1.0,
      'Parch': 0.0,
      'Fare': 75.25,
      'Embarked': 0.0,
  }

  # Test each models endpoint
  test_model(URL, "logistic_regression", data)
  test_model(URL, "random_forest", data)
