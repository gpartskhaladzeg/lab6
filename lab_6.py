import pandas as pd
import random
import xml.etree.ElementTree as ET
import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import pos_tag

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Задание 1
# Загрузите данные из файла `recipes_sample.csv` (__ЛР2__) в виде `pd.DataFrame` `recipes` 
# При помощи форматирования строк выведите информацию об id рецепта
# и времени выполнения 5 случайных рецептов в виде таблицы следующего вида:
#    
#    |      id      |  minutes  |
#    |--------------------------|
#    |    61178     |    65     |
#    |    202352    |    80     |
#    |    364322    |    150    |
#    |    26177     |    20     |
#    |    224785    |    35     |
#    
# Обратите внимание, что ширина столбцов заранее неизвестна и должна рассчитываться динамически, в зависимости от тех данных, которые были выбраны.
#
def task_1():
    recipes = pd.read_csv('data/recipes_sample.csv')
    random_recipes = recipes.sample(5)

    header = "|{:^10}|{:^10}|".format("id", "minutes")
    print(header)
    print("-" * len(header))

    for index, row in random_recipes.iterrows():
        print("|{:^10d}|{:^10d}|".format(row['id'], row['minutes']))

# Задание 2
# Напишите функцию `show_info`, которая по данным о рецепте создает строку 
# (в смысле объекта python) с описанием следующего вида:
#
# "Название Из Нескольких Слов"
# 1. Шаг 1
# 2. Шаг 2
# ----------
# Автор: contributor_id
# Среднее время приготовления: minutes минут
#    
# Данные для создания строки получите из файлов `recipes_sample.csv` (__ЛР2__)
# и `steps_sample.xml` (__ЛР3__). 
# Вызовите данную функцию для рецепта с id `170895`
# и выведите (через `print`) полученную строку на экран.
#
def parse_steps_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    steps_dict = {}
    for recipe in root.findall('recipe'):
        recipe_id = int(recipe.find('id').text)
        steps = [step.text for step in recipe.find('steps').findall('step')]
        steps_dict[recipe_id] = steps

    return steps_dict

def show_info(name, steps, minutes, author_id):
    title = name.title()
    steps_str = "\n".join(f"{i + 1}. {step}" for i, step in enumerate(steps))
    info_str = f'"{title}"\n\n{steps_str}\n----------\nАвтор: {author_id}\nСреднее время приготовления: {minutes} минут\n'
    return info_str

def task_2():
    recipes = pd.read_csv('data/recipes_sample.csv')
    steps_dict = parse_steps_xml('data/steps_sample.xml')
    recipe = recipes.loc[recipes['id'] == 170895].iloc[0]
    recipe_info = show_info(
        name=recipe['name'],
        steps=steps_dict[recipe['id']],
        minutes=recipe['minutes'],
        author_id=recipe['contributor_id']
    )
    print(recipe_info)

# Задание 3
# Напишите регулярное выражение, которое ищет следующий паттерн в строке: 
# число (1 цифра или более), затем пробел, затем слова: 
# hour или hours или minute или minutes. 
# Произведите поиск по данному регулярному выражению в каждом шаге рецепта с id 25082.
# Выведите на экран все непустые результаты, найденные по данному шаблону.
#
def task_3():
    pattern = re.compile(r'\d+\s(?:hours|hour|minutes|minute)')
    steps_dict = parse_steps_xml('data/steps_sample.xml')
    steps_25082 = steps_dict[25082]

    for step in steps_25082:
        matches = pattern.findall(step)
        if matches:
            print(matches)

# Задание 4
# Напишите регулярное выражение, которое ищет шаблон вида "this..., but" _в начале строки_ .
# Между словом "this" и частью ", but" может находиться произвольное число
# букв, цифр, знаков подчеркивания и пробелов.
# Никаких других символов вместо многоточия быть не может.
# Пробел между запятой и словом "but" может присутствовать или отсутствовать.
# Используя строковые методы `pd.Series`, выясните, для каких рецептов данный шаблон
# содержится в тексте описания. Выведите на экран количество таких рецептов
# и 3 примера подходящих описаний (текст описания должен быть виден на экране полностью).
#
def task_4():
    pd.set_option("display.max_colwidth", None)

    df = pd.read_csv("data/recipes_sample.csv")
    pattern = r"^this[\w\s]*,\s?but"
    mask = df["description"].str.contains(pattern, case=False, na=False)
    print(f"Количество рецептов с шаблоном: {mask.sum()}")
    print("Примеры описаний:")
    print("\n".join(df[mask]["description"].head(3).str.strip().to_list()))

# Задание 5
# В текстах шагов рецептов обыкновенные дроби имеют вид "a / b". 
# Используя регулярные выражения, уберите в тексте шагов рецепта с id 72367 пробелы
# до и после символа дроби. Выведите на экран шаги этого рецепта после их изменения.
#
def task_5():
    recipe_72367_steps = parse_steps_xml('data/steps_sample.xml')[72367]
    pattern = re.compile(r'\s*/\s*')

    for step in recipe_72367_steps:
        modified_step = pattern.sub('/', step)
        print(modified_step)

# Задание 6
# Разбейте тексты шагов рецептов на слова при помощи пакета `nltk`. 
# Посчитайте и выведите на экран кол-во уникальных слов среди всех рецептов. 
# Словом называется любая последовательность алфавитных символов 
# (для проверки можно воспользоваться `str.isalpha`). 
# При подсчете количества уникальных слов не учитывайте регистр.
#
def task_6():
    tree = ET.parse('data/steps_sample.xml')
    root = tree.getroot()

    unique_words = set()

    for recipe in root.findall('recipe'):
        steps = recipe.find('steps')
        for step in steps.findall('step'):
            words = word_tokenize(step.text)
            for word in words:
                if word.isalpha():
                    unique_words.add(word.lower())

    print(f"Количество уникальных слов: {len(unique_words)}")

# Задание 7
# Разбейте описания рецептов из `recipes` на предложения при помощи пакета `nltk`. 
# Найдите 5 самых длинных описаний (по количеству _предложений_) рецептов в датасете 
# и выведите строки фрейма, соответствующие этим рецептами, в порядке убывания длины.
#
def task_7():
    recipes = pd.read_csv('data/recipes_sample.csv')
    recipes['sent_count'] = recipes['description'].apply(lambda x: len(sent_tokenize(str(x))) if pd.notna(x) else 0)
    top_5_recipes = recipes.nlargest(5, 'sent_count')

    print("Топ 5 самых длинных описаний (по количеству предложений):")
    print(top_5_recipes)

# Задание 8
# Напишите функцию, которая для заданного предложения выводит 
# информацию о частях речи слов, входящих в предложение, в следующем виде:
#
#PRP   VBD   DT      NNS     CC   VBD      NNS        RB   
# I  omitted the raspberries and added strawberries instead
# 
# Для определения части речи слова можно воспользоваться `nltk.pos_tag`.
# Проверьте работоспособность функции на названии рецепта с id 241106.
# Обратите внимание, что часть речи должна находиться ровно посередине 
# над соотвествующим словом, а между самими словами должен быть ровно один пробел.
#
def display_pos(sentence):
    words = word_tokenize(sentence)
    
    pos_tags = nltk.pos_tag(words)
    
    formatted_words = []
    formatted_tags = []
    
    for word, tag in pos_tags:
        length_diff = len(word) - len(tag)
        
        if length_diff > 0:
            formatted_word = word
            formatted_tag = tag.center(len(word))
        else:
            formatted_word = word.center(len(tag))
            formatted_tag = tag
        
        formatted_words.append(formatted_word)
        formatted_tags.append(formatted_tag)
    
    word_str = ' '.join(formatted_words)
    tag_str = ' '.join(formatted_tags)
    
    print(tag_str)
    print(word_str)

def task_8():
    recipes = pd.read_csv('data/recipes_sample.csv')
    recipe_name = recipes.loc[recipes['id'] == 241106, 'name'].values[0]

    display_pos(recipe_name)

# Выполнение заданий
print("Задание 1:")
task_1()
print("\nЗадание 2:")
task_2()
print("\nЗадание 3:")
task_3()
print("\nЗадание 4:")
task_4()
print("\nЗадание 5:")
task_5()
print("\nЗадание 6:")
task_6()
print("\nЗадание 7:")
task_7()
print("\nЗадание 8:")
task_8()

