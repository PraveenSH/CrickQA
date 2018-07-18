from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn import svm
import pickle

data = pd.read_csv("../Data/type_train.csv")
data_txt = data['text']
data_label = data['label']
vectorizer = TfidfVectorizer(ngram_range=(1,2))
vec = vectorizer.fit(data_txt)
pickle.dump(vec, open("Models/type.vec",'wb'))
loaded_vec = pickle.load(open("Models/type.vec",'rb'))
X_train = loaded_vec.transform(data_txt)
Y_train = data.label
X_test = loaded_vec.transform(["most runs in test", "highest wickets in an one day match", "most t20 sixes", "highest catch"])

clf = svm.SVC(kernel='linear')
clf.fit(X_train, Y_train)
pickle.dump(clf,open("Models/type_model.sav",'wb'))
loaded = pickle.load(open("Models/type_model.sav",'rb'))
preds = loaded.predict(X_test)
print(preds)
