from django.shortcuts import render, redirect
from .forms import ReviewForm
from .models import Review
from .tasks import analyze_sentiment

def review_list(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save()
            analyze_sentiment.delay(review.id)
            return redirect('review_list')
    else:
        form = ReviewForm()
    
    reviews = Review.objects.all().order_by('-pub_date')
    return render(request, 'reviews/reviews_list.html', {
        'form': form,
        'reviews': reviews
    })