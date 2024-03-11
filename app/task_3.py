import pandas as pd

# Чтение данных из csv файла
data = pd.read_csv('products.csv')

# Создаем новый DataFrame, где индексируем данные по "Operation System"
df = data.groupby('Operation System').count()

# Сортируем данные по убыванию
df = df.sort_values('name', ascending=False)

# Данные теперь представляют распределение моделей по версиям операционных систем
print(df['name'])