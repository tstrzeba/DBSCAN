from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import matplotlib.pyplot as plt
import numpy as np
import math


def getDataForDB(categories, article_no, article_end=-1):
    # categories = ['alt.atheism', 'soc.religion.christian', 'comp.graphics', 'sci.med']

    # categories = ['comp.graphics']


    # LOAD ARTICLES
    twenty_train = fetch_20newsgroups(subset='train', categories=categories, shuffle=True, random_state=42)

    if article_no >= len(twenty_train.data):
        article_no = len(twenty_train.data) - 1

    # NOTE - ARTICLE
    # twenty_train.data -> string table with articles
    # twenty_train.filenames -> table with full path to the articles
    # print( twenty_train.data[0] )
    # print( twenty_train.filenames[0])


    # NOTE - CATEGORIES
    # twenty_train.target -> table with IDs of categories, each row corresponds to one article
    # twenty_train.target_names -> names of categories
    # for t in twenty_train.target[:10]:
    #    print(twenty_train.target_names[t])
    #
    # print(twenty_train.target[2])
    # print(twenty_train.data[2])


    # NOTE - GETTING CATEGORY FOR GIVEN ARTICLE
    # to get category of third article:
    # id_articele = 2
    # print( twenty_train.target_names[ twenty_train.target[id_articele] ])


    # print( twenty_train.data[article_no])


    if article_end <= article_no:
        one_doc = [twenty_train.data[article_no]]
    else:
        one_doc = twenty_train.data[article_no:article_end]

    print(len(one_doc))
    ## CREATE dictionary of words and its occurrences in the text
    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(one_doc)  # tewnty_train.data[0]s

    # NOTE
    # dictionary: 'word' : index of word are storing in the count_vect.vocabulary_
    # print( count_vect.vocabulary_)
    # print( list(count_vect.vocabulary_.keys())[0] )


    # NOTE
    # X_train_counts -> is the 2D table: [x,y] -> x the index of document, y -> index of word

    # print( X_train_counts)

    ## Transform to the frequency in the document
    tfidf_transformer = TfidfTransformer();
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

    # print( X_train_tfidf, "\n\n" )
    # print( X_train_tfidf.getcol(21).toarray()[0][0])


    ## creating vector for data

    # in_array_for_dbscan = []
    #
    # for i  in range(0,X_train_tfidf.shape[1] ) :
    #     in_array_for_dbscan.append([i, X_train_tfidf.getcol(i).toarray()[0][0] ])
    #
    #
    # return in_array_for_dbscan;

    # return vocabulary ( word its index ) and out matrix

    # return( count_vect.vocabulary_, X_train_tfidf )
    return (count_vect.vocabulary_, X_train_counts)


## fit testing doc data ( fit vocabulary ( words and its indexes) )
def fitTestingDictionary(training_vocab, testing_vocab, testing_outTable):
    ## 0) ustaw na pewna liczbe wszystkie indeksy w testing_vocab
    ## 1) wez 1 slowo z trainigng_vocab
    ## 2) sprawdz czy istnieje takie slowo w testing_vocab
    ## 2.1) jesli nie istnieje idź do kroku 3)
    ## 2.1) jesli istnieje to przypisz mu ten sam index i znajdz ten starty indeks w testing_outTable i zaktualizuj
    ## 3) wroc do kroku 1

    ## add 0)
    for key in testing_vocab:
        testing_vocab[key] += 12345678

    retTestingTab = []
    ## ad 1
    for key, index in training_vocab.items():

        if (key in testing_vocab):
            ## zamien index
            old_index = testing_vocab[key] - 12345678

            testing_vocab[key] = index
            ## laduj od razu z nowym indeksem do tablicy wyjsciowej
            retTestingTab.append([index, testing_outTable.getcol(old_index).toarray()[0][0]])

            # print( "\nTraining: (", key, " : ", index, " id in testing: ", old_index, " val = ", testing_outTable.getcol(old_index).toarray()[0][0])

        else:
            continue

    ## wez najwiekszy indeks z trainingu i dodaj 1 -> aby przetworzyc pozostale slowa w testowej tablicy
    app_index = max(training_vocab.values()) + 1

    ## dodaj do tablicy pozostale slowa nie bedace w tablicy training
    for key, index in testing_vocab.items():
        if index >= 12345678:
            retTestingTab.append([app_index, testing_outTable.getcol(index - 12345678).toarray()[0][0]])
            app_index += 1

    return retTestingTab


def convertTrainingRawData(training_rawData):
    in_array_for_dbscan = []

    for i in range(0, training_rawData.shape[1]):
        if training_rawData.getcol(i).toarray()[0][0] == 0:
            continue
        else:
            in_array_for_dbscan.append([i, training_rawData.getcol(i).toarray()[0][0]])

    return in_array_for_dbscan


def extendTrainingVocab(baseTraining_vocab, newSrcVocab, baseTrainingTable, newSrc_rawData):
    # dodaj wartosci wystopen slowa do baseTrainingTable
    # ii dodaj do slownika
    for key, value in newSrcVocab.items():
        if key in baseTraining_vocab:
            ## sumuj ilosc wystapien
            ## znajdz pozycje w liscie
            idx = [(i, x[0]) for i, x in enumerate(baseTrainingTable) if x[0] == value][0][0]
            # idx = -1
            # for i in range(len( baseTrainingTable )):
            #     if baseTrainingTable[i][0] == value:
            #         idx = i
            #         break

            ## odczytaj i dodaj z nowego zbioru
            newval = baseTrainingTable[idx][1] + newSrc_rawData.getcol(value).toarray()[0][0]
            ## zakutalizuj w tablicy
            baseTrainingTable[idx][1] = newval
            continue
        else:
            # dodaj do slownika nowy wyraz
            new_id = max(baseTraining_vocab.values()) + 1
            baseTraining_vocab.update({key: new_id})
            ## dodaj tez ilosc wystapien z tym indeksem do glownej tablicy
            baseTrainingTable.append([new_id, newSrc_rawData.getcol(value).toarray()[0][0]])


def getTextData():
    # use
    # (training_vocab, training_rawData) = getDataForDB(['sci.med'], 0,20) #'comp.graphics'
    # (testing_vocab, testing_rawData) = getDataForDB(['comp.graphics'],23)#['soc.religion.christian']

    (training_vocab, training_rawData) = getDataForDB(['alt.atheism'], 0)  # 'comp.graphics' # 'sci.med'
    training_tab = convertTrainingRawData(training_rawData)
    for i in range(1,30):
        (test_vocab, test_rawData) = getDataForDB(['alt.atheism'], i)  # 'comp.graphics'
        extendTrainingVocab(training_vocab, test_vocab, training_tab, test_rawData)

    (testing_vocab, testing_rawData) = getDataForDB(['alt.atheism'], 34)  # ['soc.religion.christian']
    testing_tab = fitTestingDictionary(training_vocab, testing_vocab, testing_rawData)

    # plt.plot([x[0] for x in training_tab], [y[1]/math.sqrt(30) for y in training_tab], 'o')
    # plt.plot([x[0] for x in testing_tab], [y[1] for y in testing_tab], 'ro')
    # plt.show()

    # print( "Training len: ", len(training_vocab), "\nTesting len: ", len(testing_vocab), "\n")

    # training_tab = convertTrainingRawData( training_rawData )
    # testing_tab = fitTestingDictionary(training_vocab, testing_vocab, testing_rawData)



    # #use
    # (training_vocab, training_rawData) = getDataForDB(['sci.med'], 0,20) #'comp.graphics'
    # (testing_vocab, testing_rawData) = getDataForDB(['comp.graphics'],23)#['soc.religion.christian']
    #
    # #print( "Training len: ", len(training_vocab), "\nTesting len: ", len(testing_vocab), "\n")
    #
    # training_tab = convertTrainingRawData( training_rawData )
    # testing_tab = fitTestingDictionary(training_vocab, testing_vocab, testing_rawData)
    #
    # # print ( "Training: rawData\n", training_rawData )
    # # print( "\n\n")
    # #
    # # print ( "Testing rawData\n", testing_rawData)
    # #
    # # print( "\n\nTesting out\n", testing_tab)
    # #
    # # print( "\n\nTraining out\n", training_tab)
    #
    # # testy with 20 common calculeted by 1
    #
    # # start from this one:
    #
    # #print( "\n\nMerged list:\n", sorted(out_tab, key = lambda x:x[0]))

    # plot raw points
    # plt.plot([x[0] for x in training_tab], [y[1] for y in training_tab], 'ro')
    # plt.plot([x[0] for x in testing_tab], [y[1] for y in testing_tab], 'o')
    # #plt.plot([1,2,3], [4,5,6], 'o')
    # plt.show()


    #out_tab.append([i for i in training_tab if i[1]>=1 ])
    # out_tab.append(training_tab)
    # out_tab.append(testing_tab)

    #return sorted(out_tab, key=lambda x: x[0])

    return [ [i[0], i[1]/math.sqrt(30)] for i in training_tab if i[1]/math.sqrt(30) >= 2 ] , [ i for i in testing_tab if i[1] >= 2 ] #'''+ [ i for i in testing_tab if i[1] >= 2 ]'''

# #
# data = getTextData()
# plt.plot( [x[0] for x in data], [x[1] for x in data], 'o')
# plt.show()

# # plot result of 5 different articles
# (test1_vocab, test1_rawData) = getDataForDB(['comp.graphics'], 0,20)
# # (test2_vocab, test2_rawData) = getDataForDB(['comp.graphics'], 2)
# # (test3_vocab, test3_rawData) = getDataForDB(['comp.graphics'], 5)
# # (test4_vocab, test4_rawData) = getDataForDB(['comp.graphics'], 9)
# # (test5_vocab, test5_rawData) = getDataForDB(['comp.graphics'], 13)
# print( test1_rawData)
#
# test1_tab = convertTrainingRawData( test1_rawData )
# # test2_tab = convertTrainingRawData( test2_rawData  )
# # test3_tab = convertTrainingRawData( test3_rawData  )
# # test4_tab = convertTrainingRawData( test4_rawData  )
# # test5_tab = convertTrainingRawData( test5_rawData  )
#
#
# plt.plot([x[0] for x in test1_tab], [y[1] for y in test1_tab], 'ro');
# #plt.plot([x for x in range(len(test1_tab))], sorted([y[1] for y in test1_tab], reverse=True), 'o')
# # plt.plot([x for x in range(len(test2_tab))], sorted([y[1] for y in test2_tab], reverse=True), 'o')
# # plt.plot([x for x in range(len(test3_tab))], sorted([y[1] for y in test3_tab], reverse=True), 'o')
# # plt.plot([x for x in range(len(test4_tab))], sorted([y[1] for y in test4_tab], reverse=True), 'o')
# # plt.plot([x for x in range(len(test5_tab))], sorted([y[1] for y in test5_tab], reverse=True), 'o')
# plt.show()
