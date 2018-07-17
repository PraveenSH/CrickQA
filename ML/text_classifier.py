from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn import svm

data = pd.read_csv("../Data/format_train.csv")
data_txt = data['format']
data_label = data['label']
vectorizer = TfidfVectorizer(ngram_range=(1,2))
vec = vectorizer.fit(data_txt)
X_train = vec.transform(data_txt)
Y_train = data.label
X_test = vec.transform(["test", "one day", "t20"])

clf = svm.SVC(kernel='linear')
clf.fit(X_train, Y_train)

preds = clf.predict(X_test)
print(preds)
