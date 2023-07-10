import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import ConfusionMatrixDisplay, classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import re
import string

#Get the news file
news = pd.read_excel("news.xlsx")
news.head()

#Create a numerical truth class with 2 categories
truth_class = []
for row in news['label']:
    if row == "REAL":
        truth_class.append(1)
    else:           
        truth_class.append(0)
news["truth_class"] = truth_class
news = news.sample(frac=1)
news.head()

#Plot the truth class count 
sns.countplot(x=news.truth_class,data=news,palette='Set2').set(title="Labels Count");

news.reset_index(inplace= True)
news.head()

#Remove all unnecessary columns
news.drop(columns=['index','id','title','label'],inplace=True)
news.head()

#Clean the text strings from useless/ineligible characters
def text_clean(text):
    text = text.lower()
    text = text.strip()
    text = text.capitalize()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub("\\W"," ",text) 
    text = re.sub('<.*?>+', '', text)
    text = re.sub("(http\S+)", "", text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('(\n+)', '', text)
    text = re.sub("([\w\.\-\_]+@[\w\.\-\_]+)", "", text)
    return text
news["text"] = news["text"].apply(text_clean)
news.head()

#Assign the target variable and the independent variable
x = news["text"]
y = news["truth_class"]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

#Use the vectorizer to turn the String Texts into vectors
Vectorizer = TfidfVectorizer()
Vect_x_Train = Vectorizer.fit_transform(x_train)
Vect_x_Test = Vectorizer.transform(x_test)

#Use the Logistic Regression for the model
L_Reg = LogisticRegression()
L_Reg.fit(Vect_x_Train,y_train)
L_Reg_Pred = L_Reg.predict(Vect_x_Test)

#Show the Classification report
print(classification_report(y_test, L_Reg_Pred))

#Visualize the Confusion Matrix
cm_display = ConfusionMatrixDisplay.from_estimator(L_Reg,Vect_x_Test,y_test, display_labels= ['Fake', 'Real'],cmap="YlGn");
