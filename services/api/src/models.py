from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Sentiment(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    sentiment_score = db.Column(db.Float, nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    sentence = db.Column(db.Text, nullable=False)
    created_on = db.Column(db.TIMESTAMP, server_default=db.func.now())
    updated_on = db.Column(db.TIMESTAMP, server_default=db.func.now(), server_onupdate=db.func.now())


    def __init__(self, sentence: str, sentiment_score: float, confidence: float):
        self.sentence = sentence
        self.sentiment_score = sentiment_score
        self.confidence = confidence

    @property
    def serialize(self):
        return {
            'id': self.id,
            'sentiment_score': self.sentiment_score,
            'confidence': self.confidence,
            'sentence': self.sentence,
            'created_on': self.created_on,
            'updated_on': self.updated_on
        }
