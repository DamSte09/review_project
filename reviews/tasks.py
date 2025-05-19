from celery import shared_task
from .models import Review
from transformers import pipeline
from transformers import AutoModelForSequenceClassification
# Ładowanie modelu na poziomie modułu



@shared_task(bind=True)
def analyze_sentiment(self, review_id):
    try:
        review = Review.objects.get(id=review_id)
        sentiment_pipeline = pipeline("text-classification", model="tabularisai/multilingual-sentiment-analysis")
        result = sentiment_pipeline(review.text)[0]
        review.sentiment = result['label']
        review.save()
        return {'status': 'success', 'review_id': review_id, 'review_sentiment': review.sentiment}
    except Exception as e:
        self.retry(exc=e, countdown=60)


