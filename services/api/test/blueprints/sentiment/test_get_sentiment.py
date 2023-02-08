from src.models import Sentiment


def get_sentiment_path(sentiment_id):
    return f'/sentiments/{sentiment_id}'


def test_get_sentiment_not_found(client):
    # With no sentiments in the DB

    # GET /sentiments/1001
    response = client.get(get_sentiment_path(1))

    # Should return a 404
    assert response.status_code == 404


def test_get_sentiment_invalid_id(client):
    # With no sentiments in the DB

    # GET /sentiments/<STRING>
    response = client.get(get_sentiment_path('invalid_id'))

    # Should return a 422
    assert response.status_code == 422


def test_get_sentiment_ok(client, session):
    # With a sentiment in the DB
    sentiment1 = Sentiment(sentence='star wars is the greatest movie of all time . ', sentiment_score=0.8, confidence=0.99)
    session.add(sentiment1)
    session.commit()

    # GET /sentiments/<NEW_SENTIMENT_ID>
    response = client.get(get_sentiment_path(sentiment1.id))

    # Should successfully return the sentiment
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['sentence'] == 'star wars is the greatest movie of all time . '
