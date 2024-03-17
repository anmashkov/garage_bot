import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Пример данных об автомобиле
car_data = "Марка: Toyota; Модель: Camry; Год выпуска: 2015; Цвет: белый; Пробег: 80000 км"

# Создаем объекты для работы с текстом
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
stop_words = set(stopwords.words('russian'))
lemmatizer = WordNetLemmatizer()

# Разбиваем данные на отдельные слова
words = car_data.split("; ")

# Инициализируем словарь для хранения информации об автомобиле
car_info = {}

# Проходим по каждому токену и извлекаем ключевые данные
for word in words:
    key, value = word.split(":")

    # Приводим значение к нормальной форме или лемматизируем
    if key != 'год выпуска' and key != 'пробег':
        normalized_value = lemmatizer.lemmatize(value, pos='n')
    else:
        normalized_value = value

    # Если слово не является стоп-словом, добавляем его в словарь
    if key not in stop_words:
        car_info[key] = normalized_value.strip()

# Выводим полученную информацию об автомобиле
print(car_info)