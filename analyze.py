from transformers import pipeline

# Load the classification pipeline with the specified model
pipe = pipeline("text-classification", model="tabularisai/multilingual-sentiment-analysis")
tekst_polski = "Kocham ten produkt!"  
tekst_angielski = "I hate this service."  
print(pipe(tekst_polski))  # Przykładowy wynik: [{'label': 'POSITIVE', 'score': 0.999}]  
print(pipe(tekst_angielski))
match result['label']:
            case 'Very Positive':
               review.sentiment = 'Bardzo pozytywna'
            case 'Positive':
               review.sentiment = 'Pozytywna'   
            case 'Neutral':
               review.sentiment = 'Neutralna'
            case 'Negative':
               review.sentiment = 'Negatywna'
            case 'Very Negative':
               review.sentiment = 'Bardzo negatywna'