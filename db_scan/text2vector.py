from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np


def getDataForDB( article_no ):


    #categories = ['alt.atheism', 'soc.religion.christian', 'comp.graphics', 'sci.med']
    categories = ['comp.graphics']


    #LOAD ARTICLES
    twenty_train = fetch_20newsgroups(subset='train', categories=categories, shuffle=True, random_state=42)

    if article_no >= len(twenty_train.data):
        article_no = len(twenty_train.data) -1

    #NOTE - ARTICLE
    # twenty_train.data -> string table with articles
    # twenty_train.filenames -> table with full path to the articles
    #print( twenty_train.data[0] )
    #print( twenty_train.filenames[0])


    #NOTE - CATEGORIES
    # twenty_train.target -> table with IDs of categories, each row corresponds to one article
    # twenty_train.target_names -> names of categories
    # for t in twenty_train.target[:10]:
    #    print(twenty_train.target_names[t])
    #
    # print(twenty_train.target[2])
    # print(twenty_train.data[2])


    #NOTE - GETTING CATEGORY FOR GIVEN ARTICLE
    # to get category of third article:
    # id_articele = 2
    # print( twenty_train.target_names[ twenty_train.target[id_articele] ])


    #print( twenty_train.data[article_no])
    ## CREATE dictionary of words and its occurrences in the text
    one_doc = [ twenty_train.data[article_no] ]
    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(one_doc) #tewnty_train.data[0]

    #NOTE
    # dictionary: 'word' : index of word are storing in the count_vect.vocabulary_
   # print( count_vect.vocabulary_)
    #print( list(count_vect.vocabulary_.keys())[0] )


    #NOTE
    # X_train_counts -> is the 2D table: [x,y] -> x the index of document, y -> index of word

    #print( X_train_counts)

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

    #@return( count_vect.vocabulary_, X_train_tfidf )
    return ( count_vect.vocabulary_, X_train_counts)


## fit testing doc data ( fit vocabulary ( words and its indexes) )
def fitTestingDictionary( training_vocab, testing_vocab, testing_outTable):
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
        if ( key in testing_vocab ):
            ## zamien index
            old_index = testing_vocab[key] - 12345678
            testing_vocab[key] = index
            ## laduj od razu z nowym indeksem do tablicy wyjsciowej
            retTestingTab.append([index, testing_outTable.getcol(old_index).toarray()[0][0]])
        else:
            continue




    ## wez najwiekszy indeks z trainingu i dodaj 1 -> aby przetworzyc pozostale slowa w testowej tablicy
    app_index = max( training_vocab.values() ) + 1

    ## dodaj do tablicy pozostale slowa nie bedace w tablicy training
    for key, index in testing_vocab.items():
        if index >= 12345678:
            retTestingTab.append([app_index, testing_outTable.getcol(index-12345678).toarray()[0][0]])
            app_index += 1



    return retTestingTab





def convertTrainingRawData( training_rawData ):
    in_array_for_dbscan = []

    for i  in range(0,training_rawData.shape[1] ) :
        in_array_for_dbscan.append([i, training_rawData.getcol(i).toarray()[0][0] ])

    return in_array_for_dbscan



#use
(training_vocab, training_rawData) = getDataForDB(0)
(testing_vocab, testing_rawData) = getDataForDB(1)

print( "Training len: ", len(training_vocab), "\nTesting len: ", len(testing_vocab), "\n")

training_tab = convertTrainingRawData( training_rawData )
testing_tab = fitTestingDictionary(training_vocab, testing_vocab, testing_rawData)

print ( "Training: rawData\n", training_rawData )
print( "\n\n")

print ( "Testing rawData\n", testing_rawData)

print( "\n\nTesting out\n", testing_tab)

print( "\n\nTraining out\n", training_tab)