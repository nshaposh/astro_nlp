from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import classification_report as clsr
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split as tts
import time
from preprocess import Preprocess
#from sklearn.manifold import
#from sklearn.decomposition import TruncatedSVD



class ABSClassifier:
    """ The classifier to initiate and fit the abstract classification model"""
#    identity = lambda x: x

    def __init__(self, classifier = SGDClassifier, ngram_range = (1,2)):

        if isinstance(classifier, type):
            classifier = classifier()
 
        self.model = Pipeline([
            ('preprocessor', Preprocess()),
            ('vectorizer', TfidfVectorizer(
                tokenizer=lambda x: x, preprocessor=None, lowercase=False, ngram_range = ngram_range
            )),
            ('classifier', classifier),
        ])     
        self.fitted = False
        

    def fit(self, X, y, split = False, test_size = 0.2):
        """
        Fit the model. 
        If split is True, split the input array into train and test with tts
        according to test_size
        """
        # Label encode the targets
        self.labels_ = LabelEncoder()
        y_labels = self.labels_.fit_transform(y)

        if split:
            X_train, X_test, y_train, y_test = tts(X, y_labels, test_size=0.2)
        else:
            X_train, X_test, y_train, y_test = X,[],y_labels,[]

        t0 = time.time()            
        self.model.fit(X_train, y_labels)
        print("Done fitting the model in {} sec.".format(time.time()-t0))
        self.fitted = True
        if split:
            y_pred = model.predict(X_test)
            print(clsr(y_test, y_pred, target_names=self.labels.classes_))

    def predict(self, X):
        
        return self.model.predict(X)
    

