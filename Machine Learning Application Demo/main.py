from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import json
import pandas as pd 
from urllib.parse import unquote  

with open('data.json', 'r') as f:
    data = json.load(f)
    
    
df = pd.DataFrame(data)

df['url'] = df['url'].apply(unquote)  

df['x1'] = df['method']
df['x2'] = df['url']
df['x3'] = df['data']

X = df[['x1', 'x2', 'x3']]
y = df['isAttack']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

preprocessor = ColumnTransformer(
    transformers=[
        ('method', TfidfVectorizer(), 'x1'),
        ('url', TfidfVectorizer(), 'x2'),
        ('data', TfidfVectorizer(), 'x3')
    ])

model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression())
])

model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("Doğruluk Skoru:", accuracy_score(y_test, y_pred))
print("\nSınıflandırma Raporu:\n", classification_report(y_test, y_pred))


manual_test_data = pd.DataFrame({
    'x1': ['GET'],  
    'x2': ['/<script>alert(1)</script>'],  
    'x3': ['']  
})


y_pred_manual = model.predict(manual_test_data)


print("\nManuel Test Sonucu:")
print(f'Tahmin: {y_pred_manual[0]}')  

manual_test_data = pd.DataFrame({
    'x1': ['GET'],
    'x2': ['/home/users?id=3'],
    'x3': ['']
})

y_pred_manual = model.predict(manual_test_data)

print("\nManuel Test Sonucu:")
print(f'Tahmin: {y_pred_manual[0]}')  

manual_test_data = pd.DataFrame({
    'x1': ['GET'],
    'x2': ['/?p={{constructor.constructor(''prompt(2)'')()}}'],
    'x3': ['']
})

y_pred_manual = model.predict(manual_test_data)

print("\nManuel Test Sonucu:")
print(f'Tahmin: {y_pred_manual[0]}') 
