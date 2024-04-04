import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib
class datamodel:
    
    def __init__(self): # Loading in the model file (this includes all weights after training) / needs to be re-run every time
        self.model = joblib.load("College_prediction.pkl")
    def readfile(self): # one and done since it just obtains training data once and for all
        self.data=pd.read_csv("college_dataset.csv")
        print(self.data.head())
    def preprocessing(self):# this is loading in the file stuff into X and Y / one and done because we're just defining variables
        self.X=self.data[['GPA','SAT_Score','Extracurricular_Activities']]
        self.Y=self.data['Admission_Status']
    def train(self): # this is actually training the model / one and done; no need to re-train every time
        self.model=LogisticRegression()
        self.model.fit(self.X,self.Y)
        
    def exportmodel(self): # after training the model, we have to export to permanently save weights to .pkl file / one and done
        joblib.dump(self.model,"College_prediction.pkl")
        
    def predict(self, GPA, SAT_SCORE, EXTRACIRICULAR): # this is prediciton function
        return self.model.predict([[GPA, SAT_SCORE, EXTRACIRICULAR]])[0]
    

    ## this stuff is just crud 
        
    def create(self, new_data):
        self.data = self.data.append(new_data, ignore_index=True)
        
    def read(self):
        return self.data
    
    def update(self, index, updated_data):
        self.data.loc[index] = updated_data
        
    def delete(self, index):
        self.data.drop(index, inplace=True)
    
    
Model=datamodel()# sample class thing
# Model.readfile()
# Model.preprocessing()  # No need of training everytime; obtains data from .pkl file everytime prediction is run
# Model.train()
Model.exportmodel()
print(Model.predict(4.0,1600,8))# sample Prediction