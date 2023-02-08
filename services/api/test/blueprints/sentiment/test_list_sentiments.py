from src.models import Sentiment

LIST_SENTIMENTS_PATH = '/sentiments/'
path_create_review = "/sentiments/create_review"

def test_list_sentiments_empty(client):
    # With no sentiments in the DB

    # GET /sentiments/
    response = client.get(LIST_SENTIMENTS_PATH)

    # Should successfully return an empty array
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data) == 0


def test_list_sentiments_non_empty(client, session):
    # With sentiments in the DB
    sentiment1 = Sentiment(sentence='Harry Potter is a wretched movie', sentiment_score=-0.01, confidence=0.92)
    sentiment2 = Sentiment(sentence='Harry Potter is an amazing movie', sentiment_score=0.95, confidence=0.99)
    session.add(sentiment1)
    session.add(sentiment2)
    session.commit()

    # GET /sentiments/
    response = client.get(LIST_SENTIMENTS_PATH)

    # Should successfully return a non-empty array
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data) == 2

def test_no_request_body(client):
    response = client.post(path_create_review) 
    assert response.status_code == 422