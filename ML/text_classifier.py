from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn import svm
import pickle

def train(inp):
    data = pd.read_csv("../Data/"+inp+"_train.csv")
    data_txt = data['text']
    data_label = data['label']
    vectorizer = TfidfVectorizer(ngram_range=(1,2))
    vec = vectorizer.fit(data_txt)
    pickle.dump(vec, open("Models/"+inp+".vec",'wb'))
    X_train = vec.transform(data_txt)
    Y_train = data.label

    clf = svm.SVC(kernel='linear')
    clf.fit(X_train, Y_train)
    pickle.dump(clf,open("Models/"+inp+"_model.sav",'wb'))

def test(inp):

    loaded_model = pickle.load(open("Models/"+inp+"_model.sav",'rb'))
    loaded_vec = pickle.load(open("Models/"+inp+".vec",'rb'))
    X_test = loaded_vec.transform(["most wickets in test", "bowler with best average", "most t20 five fors", "highest no. of 4 fors", "best bowling performance", "top economic bowler"])
    preds = loaded_model.predict(X_test)
    print(preds)

cls = ["batting", "bowling", "format", "type", "fielding"]
for cl in cls:
    train(cl)
