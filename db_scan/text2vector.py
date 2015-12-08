from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


def getDataForDB( article_no ):

    categories = ['alt.atheism', 'soc.religion.christian', 'comp.graphics', 'sci.med']


    #LOAD ARTICLES
    twenty_train = fetch_20newsgroups(subset='train', categories=categories, shuffle=True, random_state=42)

    if article_no >= len(twenty_train.data):
        article_no = len(twenty_train.data) -1 ;

    #NOTE - ARTICLE
    # twenty_train.data -> string table with articles
    # twenty_train.filenames -> table with full path to the articles
    #print( twenty_train.data[0] )
    #print( twenty_train.filenames[0])


    #NOTE - CATEGORIES
    # twenty_train.target -> table with IDs of categories, each row corresponds to one article
    # twenty_train.target_names -> names of categories
    # for t in twenty_train.target[:10]:
    #    print(twenty_train.target_names[t]);


    #NOTE - GETTING CATEGORY FOR GIVEN ARTICLE
    # to get category of third article:
    # id_articele = 2
    # print( twenty_train.target_names[ twenty_train.target[id_articele] ])


    ## CREATE dictionary of words and its occurrences in the text
    one_doc = [ twenty_train.data[article_no] ]
    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(one_doc) #tewnty_train.data[0]

    #NOTE
    # dictionary: 'word' : occurrences are storing in the count_vect.vocabulary_
    #print( count_vect.vocabulary_)
    #print( list(count_vect.vocabulary_.keys())[0] )


    #NOTE
    # X_train_counts -> is the 2D table: [x,y] -> x the index of document, y -> index of word

    #print( X_train_counts)

    ## Transform to the frequency in the document
    tfidf_transformer = TfidfTransformer();
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)




    ## creating vector for data

    in_array_for_dbscan = []

    for i  in range(0,X_train_tfidf.shape[1] ) :
        in_array_for_dbscan.append([i, X_train_tfidf.getcol(i).toarray()[0][0] ])


    return in_array_for_dbscan;


#use
print( getDataForDB(30) )