# Scaling the features

# features_to_scale = [] --> list of features to scale
# X_train = pd.DataFrame() --> pd dataframe of training data
# X_val = pd.DataFrame() --> pd dataframe of validation data
# X_test = pd.DataFrame()--> pd dataframe of test data



def feature_scaler(features_to_scale, X_train, X_val, X_test):
    from sklearn.preprocessing import MinMaxScaler

    # Initialize scaler
    scaler = MinMaxScaler()
    
    # Fit scaler on X_train
    scaler.fit(X_train[features_to_scale])
    
    # Transform X_train
    X_train.loc[:, features_to_scale] = scaler.transform(X_train[features_to_scale])
    
    # Transform X_val
    X_val.loc[:, features_to_scale] = scaler.transform(X_val[features_to_scale])
    
    # Transform X_test
    X_test.loc[:, features_to_scale] = scaler.transform(X_test[features_to_scale])
    
    return X_train, X_val, X_test, scaler