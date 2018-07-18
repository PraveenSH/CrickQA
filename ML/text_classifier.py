from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn import svm
import pickle

data = pd.read_csv("../Data/format_train.csv")
data_txt = data['text']
data_label = data['label']
vectorizer = TfidfVectorizer(ngram_range=(1,2))
vec = vectorizer.fit(data_txt)
X_train = vec.transform(data_txt)
Y_train = data.label
X_test = vec.transform(["most runs in test", "highest wickets in an one day match", "most t20 sixes", "highest catch"])

clf = svm.SVC(kernel='linear')
clf.fit(X_train, Y_train)
pickle.dump(clf,open("Models/format_model.sav",'wb'))
loaded = pickle.load(open("Models/format_model.sav",'rb'))
preds = loaded.predict(X_test)
print(preds)
