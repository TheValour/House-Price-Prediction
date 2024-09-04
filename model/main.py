import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import pickle;

def clean_data(df):
    df = df.replace({
        'yes': 1,
        'no': 0,
        'furnished': 1,
        'semi-furnished': 2,
        'unfurnished': 3
    })
    return df

def encode_features(df, column):
    ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=False).set_output(transform='pandas')
    ohe_data = ohe.fit_transform(df[[column]])
    df = pd.concat([df.drop(columns=[column]), ohe_data], axis=1)
    return df


def trainModel(df):
    y = df['price']
    X = df.drop(columns=['price'])

    # scaling the data
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    # spilliting the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)  

    # train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("Predicted value : ", r2_score(y_test, y_pred))

    return model, scaler


def main():
    # Load and clean data-------------
    df = pd.read_csv('E:\\Programming\\python\\data\\Housing.csv')
    df = clean_data(df)

    # Encode categorical features
    df = encode_features(df, 'furnishingstatus')

    model, scaler = trainModel(df)

    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    with open('scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)

if __name__ == "__main__":
    main()
