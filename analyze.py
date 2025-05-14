from transformers import pipeline  
pipe = pipeline("text-classification", model="tabularisai/multilingual-sentiment-analysis")  
tekst_polski = "Kocham ten produkt!"  
tekst_angielski = "I hate this service."  
print(pipe(tekst_polski))  # Przykładowy wynik: [{'label': 'POSITIVE', 'score': 0.999}]  
print(pipe(tekst_angielski))