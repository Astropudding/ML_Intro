# объявим где хранятся исходные данные
PATH_TRAIN = '../input/train.csv'
#PATH_TEST = '../input/test.csv'
PATH_TEST = '../input/1.txt'

# объявим куда сохраним результат
#PATH_PRED = 'pred.csv'
PATH_PRED = '1.csv'


## Из тренировочного набора собираем статистику о встречаемости слов

# создаем словарь для хранения статистики
word_stat_dict = {}

# открываем файл на чтение в режиме текста
fl = open(PATH_TRAIN, 'rt')

# считываем первую строчку - заголовок (она нам не нужна)
fl.readline()

# в цикле читаем строчки из файла
for line in fl:
    # разбиваем строчку на три строковые переменные
    Id, Sample, Prediction = line.strip().split(',')
    # строковая переменная Prediction - содержит в себе словосочетание из 2 слов, разделим их
    word1, word2 = Prediction.split(' ')
    # возьмем в качестве ключа 2 первые буквы, т.к. их наличие гарантировано
    key = word2[:2]
    # если такого ключа еще нет в словаре, то создадим пустой словарь для этого ключа
    if key not in word_stat_dict:
        word_stat_dict[key] = {}
    # если текущее слово еще не встречалось, то добавим его в словарь и установим счетчик этого слова в 0
    if word2 not in word_stat_dict[key]:
        word_stat_dict[key][word2] = 0
    # увеличим значение счетчика по текущему слову на 1
    word_stat_dict[key][word2] += 1

    key = word1[:2]
    # если такого ключа еще нет в словаре, то создадим пустой словарь для этого ключа
    if key not in word_stat_dict:
        word_stat_dict[key] = {}
    # если текущее слово еще не встречалось, то добавим его в словарь и установим счетчик этого слова в 0
    if word1 not in word_stat_dict[key]:
        word_stat_dict[key][word1] = 0
    # увеличим значение счетчика по текущему слову на 1
    word_stat_dict[key][word1] += 1

# закрываем файл
fl.close()

## Строим модель

# создаем словарь для хранения статистики
most_freq_dict = {}

# проходим по словарю word_stat_dict
for key in word_stat_dict:
    # для каждого ключа получаем наиболее часто встречающееся (наиболее вероятное) слово и записываем его в словарь most_freq_dict
    most_freq_dict[key] = max(word_stat_dict[key], key=word_stat_dict[key].get)


## Выполняем предсказание

# открываем файл на чтение в режиме текста
fl = open(PATH_TEST, 'rt')

# считываем первую строчку - заголовок (она нам не нужна)
fl.readline()

# открываем файл на запись в режиме текста
out_fl = open(PATH_PRED, 'wt')

# записываем заголовок таблицы
out_fl.write('Id,Prediction\n')

# в цикле читаем строчки из тестового файла
for line in fl:
    # разбиваем строчку на две строковые переменные
    Id, Sample = line.strip().split(',')
    # строковая переменная Sample содержит в себе полностью первое слово и кусок второго слова, разделим их
    word1, word2_chunk = Sample.split(' ')
    # вычислим ключ для заданного фрагмента второго слова
    key = word2_chunk[:2]
    if key in word_stat_dict:
        print (word_stat_dict[key])
        # если ключ есть в нашем словаре, пишем в файл предсказаний: Id, первое слово, наиболее вероятное второе слово
        some_words = {k : word_stat_dict[key][k] for k in word_stat_dict[key] if word2_chunk in k}
        if some_words:
            out_fl.write('%s,%s %s\n' % (Id, word1, max(some_words, key=some_words.get)))
        else:
            out_fl.write('%s,%s %s\n' % (Id, word1, most_freq_dict[key]) )
    else:
        # иначе пишем наиболее часто встречающееся словосочетание в целом
        out_fl.write('%s,%s\n' % (Id, 'что она') )

# закрываем файлы
fl.close()
out_fl.close()
