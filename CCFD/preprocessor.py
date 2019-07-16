from scipy.io import arff
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from MultiColumnLabelEncoder import MultiColumnLabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("credit-g.csv")
'''
checking_status,duration,credit_history,purpose,credit_amount,savings_status,employment,
installment_commitment,personal_status,other_parties,residence_since,property_magnitude,age, 
other_payment_plans,housing,existing_credits,job,num_dependents,own_telephone, foreign_worker,
class
'''
print(data.head())
'''
category = [
    [0,1,1,0],
    [],
    [0,0,0,1,1],
    [0,0,0,0,0,0,0,0,0,0],
    [],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0],
    []
]
'''
#print(data.head())
#sns.countplot(x='class', hue='personal_status', data=data)
#plt.title('class distribution')
#plt.show()
numerical_index = [1, 4, 7, 10, 12, 15, 17]
data_class = data['class']
data_numerical = data[data.columns[numerical_index]]
data.drop(data.columns[numerical_index], axis=1, inplace=True)
data.drop('class', axis=1, inplace=True)
print(data_numerical.head())

le = MultiColumnLabelEncoder()
encoded_array = le.fit_transform(data)

#enc = OneHotEncoder()
#encoded_array = enc.fit_transform(data).toarray()

print(encoded_array)