from celery import shared_task
from .models import Review
from transformers import pipeline
from transformers import AutoModelForSequenceClassification
# Ładowanie modelu na poziomie modułu
import redis
import json

redis_client = redis.Redis(host='localhost', port=6379, db=0)


_model = None

def get_model():
    global _model
    if _model is None:
        print("Ładowanie modelu...")
        _model = pipeline("text-classification", model="tabularisai/multilingual-sentiment-analysis")
    return _model


@shared_task(bind=True)
def analyze_sentiment(self, review_id):
    try:
        review = Review.objects.get(id=review_id)
        cache_key = f"sentiment:review:{review_id}"

        # Sprawdź cache
        cached_sentiment = redis_client.get(cache_key)
        if cached_sentiment:
            sentiment_label = cached_sentiment.decode('utf-8')
            review.sentiment = sentiment_label
            review.save()
            return {
                'status': 'cached',
                'review_id': review_id,
                'review_sentiment': sentiment_label
            }

        # Jeśli nie ma w cache, wykonaj analizę
        sentiment_pipeline = get_model()
        result = sentiment_pipeline(review.text)[0]
        sentiment_label = result['label']

        # Zapisz do bazy danych
        review.sentiment = sentiment_label
        review.save()

        # Zapisz wynik do Redis
        redis_client.set(cache_key, sentiment_label, ex=60 * 60 * 24)  # 24 godziny

        return {
            'status': 'success',
            'review_id': review_id,
            'review_sentiment': sentiment_label
        }

    except Exception as e:
        self.retry(exc=e, countdown=60)


