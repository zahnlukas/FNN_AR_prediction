import pandas as pd
import numpy as np



### Preprocessing function ###

def preprocessing(df):
    
    df['receipt_date']=pd.to_datetime(df['receipt_date'],format='%Y-%m-%d')
    df['due_date']=pd.to_datetime(df['due_date'],format="%Y-%m-%d")
    df['weighted_payment_date']=pd.to_datetime(df['weighted_payment_date'],format='%Y-%m-%d')
    
    df = df.sort_values('receipt_date')  
    rows_before = len(df)
    
    # Select date range of whole dataset 
    def select_date_range(df):
        df = df[(df['receipt_date'] >= '2022-01-01') & (df['receipt_date'] <= '2024-05-01')]
        return df
    
    #remove missing values
    def remove_missing_values(df):
        df = df.dropna()
        return df
    
    def remove_false_entries(df):                #No prediction needed if payment already made
        df = df[df['weighted_payment_date'] > df['receipt_date']]
        df = df[df['due_date'] > df['receipt_date']]
        return df
    
    
    #log transform amount_euro column, since normal amount columns is replaced by amount_euro
    def amount_column(df):
        df = df[df['amount_euro'] >= 1] 
        df.loc[:, 'log_amount'] = np.log(df['amount_euro'])
        return df
    
    def payment_term_column(df):
        df = df[df["payment_terms"] <= 120]
        return df
        
   
    #create "dso" column & remove outliers:
    def dso_creator(df):
          df['dso'] = (df['weighted_payment_date'] - df['receipt_date']).dt.days
          df = df[df["dso"] <= 120]
          return df
      
    def dbt_creator(df):
        df['dbt'] = (df['weighted_payment_date'] - df['due_date']).dt.days


        return df
      
      
     
      # Apply the preprocessing steps
    df = select_date_range(df)
    df = remove_false_entries(df)
    df = remove_missing_values(df)
    df = amount_column(df)
    df = payment_term_column(df)
    df = dso_creator(df)
    df = dbt_creator(df)

    
    rows_after = len(df)
    
    print(f"Number of rows before preprocessing: {rows_before}")
    print(f"Number of rows after preprocessing: {rows_after}")
    
    return df















    



        
        



