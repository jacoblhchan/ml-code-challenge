from flask import Blueprint, request
from flask.json import jsonify
from src.models import Sentiment, db
from src.sentiment_analyzer.sentiment_analysis import SentimentAnalysis
from transformers import pipeline

sentiment_blueprint = Blueprint('sentiment', __name__, url_prefix='/sentiments')
model= SentimentAnalysis()

@sentiment_blueprint.route('/', methods=['GET'])
def index():
    sentiments = Sentiment.query.all()
    return jsonify([sentiment.serialize for sentiment in sentiments])


@sentiment_blueprint.route('/<sentiment_id>', methods=['GET'])
def get(sentiment_id):
    if not sentiment_id.isdigit():
        return jsonify({'message': 'id must be an integer'}), 422

    sentiment = Sentiment.query.get(sentiment_id)

    if not sentiment:
        return jsonify({'message': 'Sentiment not found.'}), 404

    return jsonify(sentiment.serialize)


@sentiment_blueprint.route('/create_review', methods=['POST'])
def create_review():
    sentence = request.args.get('sentence')
    if sentence is None:
        return jsonify({'message': 'review must be provided'}), 422
    sentiment = get_result(sentence)
    return jsonify(sentiment.serialize), 201

def get_result(sentence:str)-> Sentiment:
    #Do we care about duplicate? if so add a step to check if record exist in DB
    sentiment_score, confidence = model.run(sentence)
    sentiment = Sentiment(sentence, sentiment_score, confidence)
    db.session.add(sentiment)
    db.session.commit()
    return sentiment