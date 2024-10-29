import pandas as pd
import numpy as np
from datetime import timedelta



# Rolling average of DSO: average dso of customer for last w months
def calculate_rolling_avg(df, w):
    df = df.sort_values(['customer_id', 'weighted_payment_date']) #sort by payment date to avoid data leakage
    df['rolling_avg_dso'] = None
    w_days = w * 30

    # Get the unique customer IDs
    customer_ids = df['customer_id'].unique()

    # For each customer ID
    for customer_id in customer_ids:       
        # Get the rows for this customer
        customer_rows = df[df['customer_id'] == customer_id]

        # For each row in the customer's data
        for i in range(len(customer_rows)):
            # If it's the first row for the current customer
            if i == 0:
                # Set 'avg_dbt_update' equal to 'dso'
                df.loc[customer_rows.index[i], 'rolling_avg_dso'] = customer_rows.iloc[i]['dso']          ## Assumption: we can make prediction only if we have at least one invoice paid by the customer
                
                   # else if the receipt_date is the same as previous one, take the previous row's 'rolling_avg_dso' value
            elif customer_rows.iloc[i]['receipt_date'] == customer_rows.iloc[i-1]['receipt_date']:
                df.loc[customer_rows.index[i], 'rolling_avg_dso'] = df.loc[customer_rows.index[i-1], 'rolling_avg_dso']
                
            else:
                # Get the current date
                current_date = customer_rows.iloc[i]['receipt_date']                        ## receipt_date since we have it on new invoice   

                # Get the receipts, that were paid within w months before the current date
                start_date = current_date - timedelta(days=w_days)
                previous_rows = customer_rows[(customer_rows['weighted_payment_date'] >= start_date) & (customer_rows['weighted_payment_date'] < current_date)] # weighted_payment_date s.t. it only takes into account invoices that were paid in last w months

                # if previous_rows is empty, then take the previous row's 'avg_dbt_update' value
                if previous_rows.empty:
                    df.loc[customer_rows.index[i], 'rolling_avg_dso'] = df.loc[customer_rows.index[i-1], 'rolling_avg_dso']
                else:
                    # Calculate the average 'dso' for these rows
                    avg_dso = previous_rows['dso'].mean()

                    # Set the rolling average for the current row
                    df.loc[customer_rows.index[i], 'rolling_avg_dso'] = avg_dso

    return df


#Creates:
#   near_payment_term_count: The number of payments made in the last w months that are within 4 days of the payment term
#   near_payment_term_ratio: The ratio of near_payment_term_count to the total number of payments made in the last w months
#   overdue_ratio: The ratio of payments made in the last w months that are overdue to the total number of payments made in the last w months


# inputs:   months to look back: w & days to consider payment overdue: v
def payment_behaviour(df, w, v):
    """
    payment_behavviour creates the following features
    near_payment_term_count: The number of payments made in the last w months that are within 4 days of the payment term
    near_payment_term_ratio: The ratio of near_payment_term_count to the total number of payments made in the last w months
    overdue_ratio: The ratio of payments made in the last w months that are overdue to the total number of payments made in the last w months
    """
    
    
    df = df.sort_values(['customer_id', 'weighted_payment_date']) #sort by payment date to avoid data leakage
    
    
    # Initialize a new column for the rolling average
    df['near_payment_term_count'] = None
    df['near_payment_term_ratio'] = None
    df['overdue_ratio'] = None


    # Convert w to days
    w_days = w * 30

    # Get the unique customer IDs
    customer_ids = df['customer_id'].unique()

    # For each customer ID
    for customer_id in customer_ids:
        
        #print(customer_id)
        # Get the rows for this customer
        customer_rows = df[df['customer_id'] == customer_id]

        # For each row in the customer's data
        for i in range(len(customer_rows)):
            
            # If it's the first row for the current customer
            if i == 0:
                # Set "near_payment_term_count" = 0 
                df.loc[customer_rows.index[i], 'near_payment_term_count'] = 0
                df.loc[customer_rows.index[i], 'near_payment_term_ratio'] = 0
                df.loc[customer_rows.index[i], 'overdue_ratio'] = 0

                
                # else if the receipt_date is the same as previous one, then take the previous row's 'near_payment_term_count' value
            elif customer_rows.iloc[i]['receipt_date'] == customer_rows.iloc[i-1]['receipt_date']:
                df.loc[customer_rows.index[i], 'near_payment_term_count'] = df.loc[customer_rows.index[i-1], 'near_payment_term_count']
                df.loc[customer_rows.index[i], 'near_payment_term_ratio'] = df.loc[customer_rows.index[i-1], 'near_payment_term_ratio']
                df.loc[customer_rows.index[i], 'overdue_ratio'] = df.loc[customer_rows.index[i-1], 'overdue_ratio']
                 
            else:
                # Get the current date
                current_date = customer_rows.iloc[i]['receipt_date']    ## receipt_date since we have it on new invoice   

                # Get the rows that are within w months before the current date
                start_date = current_date - timedelta(days=w_days)
                previous_rows = customer_rows[(customer_rows['weighted_payment_date'] >= start_date) & (customer_rows['weighted_payment_date'] < current_date)]

                # if previous_rows is empty, then take the previous row's 'near_payment_term_count' value
                if previous_rows.empty:
                    df.loc[customer_rows.index[i], 'near_payment_term_count'] = df.loc[customer_rows.index[i-1], 'near_payment_term_count']
                    df.loc[customer_rows.index[i], 'near_payment_term_ratio'] = df.loc[customer_rows.index[i-1], 'near_payment_term_ratio']
                    df.loc[customer_rows.index[i], 'overdue_ratio'] = df.loc[customer_rows.index[i-1], 'overdue_ratio']

                    
                else:
                    # store the count of payments in last w monts for the ratio calculation
                    count = len(previous_rows)
                    count_overdue = len(previous_rows[previous_rows['dbt'] > v])
                    overdue_ratio = count_overdue / count

                    
                    # store the count of payments in last w months that are "near_payment_term"
                    previous_rows_near_payment_term = previous_rows[
                        (previous_rows['dso'] >= previous_rows["payment_terms"] - 4) &
                        (previous_rows['dso'] <= previous_rows["payment_terms"] + 4)] 
            
                    count_near_payment_term = len(previous_rows_near_payment_term)
                    
                    # calculate the near payment term ratio
                    near_payment_term_ratio = count_near_payment_term / count
                    
                    # Set the near payment term count and ratio for the current row
                    df.loc[customer_rows.index[i], 'near_payment_term_count'] = count_near_payment_term
                    df.loc[customer_rows.index[i], 'near_payment_term_ratio'] = near_payment_term_ratio
                    
                    #Set the overdue ratio for the current row
                    df.loc[customer_rows.index[i], 'overdue_ratio'] = overdue_ratio
                                    
    return df




# My code: Define outstanding invoice as features with receipt_date < current_receipt_date in last w months that have weighted_payment_date > current_receipt_date, meaning they are not paid at the moment of current receipt
# When applied to reality: Outstanding features where receipt_date < current_receipt_date in last w months & weighted_payment_date empty

def calculate_outstanding_invoices(df, w):
    df = df.sort_values(['customer_id', 'weighted_payment_date'])   #sort by payment date to avoid data leakage
    
    """
    outstanding_invoices: count of invoices issued in last w months that are not paid yet
    paid_invoices: The total number of payments made in the last w months
    """

    # Initialize a new column for the outstending_invoices
    df['outstanding_invoices'] = 0
    df['paid_invoices'] = 0
    df["issued_invoices"] = 0

    
    # Convert w to days
    w_days = w * 30

    # Get the unique customer IDs
    customer_ids = df['customer_id'].unique()
    
        # For each customer ID
    for customer_id in customer_ids:
        
        #to track the progress
        #print(customer_id)
        
        # Get the rows for this customer
        customer_rows = df[df['customer_id'] == customer_id]
        
        # For each row in the customer's data
        for i in range(len(customer_rows)):
            # If it's the first row for the current customer
            if i != 0:
                # Get the current date
                current_date = customer_rows.iloc[i]['receipt_date']    ## receipt_date since we have it on new invoice   

                # Get the rows that are within w months before the current date that are not paid
                start_date = current_date - timedelta(days=w_days)
                previous_rows_open = customer_rows[(customer_rows['receipt_date'] >= start_date) &
                                              (customer_rows['receipt_date'] < current_date) &
                                              (customer_rows['weighted_payment_date'] > current_date)]
                previous_rows_paid = customer_rows[(customer_rows['weighted_payment_date'] >= start_date) & (customer_rows['weighted_payment_date'] < current_date)]
                previous_rows_issued = customer_rows[(customer_rows['receipt_date'] >= start_date) & (customer_rows['receipt_date'] < current_date)]
                
                
                # Set outstanding_invoices and paid_invoices
                df.loc[customer_rows.index[i], 'outstanding_invoices'] = len(previous_rows_open)
                df.loc[customer_rows.index[i], 'paid_invoices'] = len(previous_rows_paid)
                df.loc[customer_rows.index[i], 'issued_invoices'] = len(previous_rows_issued)

    return df


def ratio_outstanding(df):
    df["ratio_outstanding"] = df.apply(lambda row: 0 if row['issued_invoices'] == 0 else row['outstanding_invoices'] / row['issued_invoices'], axis=1)
    
    return df


def binning_counts(df):
    bins = [float("-inf"), 3,10, float("inf")]
    labels = [0, 1, 2]
    
    # Binning the counts
    df['near_payment_term_count_binned'] = pd.cut(df['near_payment_term_count'], bins=bins, labels=labels)
    df["paid_invoices_binned"] = pd.cut(df['paid_invoices'], bins=bins, labels=labels)
    df["outstanding_invoices_binned"] = pd.cut(df['outstanding_invoices'], bins=bins, labels=labels)

    
    return df


def binarize_counts(df):
    
    df["binary_paid_invoices"] = df['paid_invoices'].apply(lambda x: 1 if x > 10 else 0)
    df["binary_outstanding_invoices"] = df['outstanding_invoices'].apply(lambda x: 1 if x > 10 else 0)
    df["binary_near_payment_term_count"] = df['near_payment_term_count'].apply(lambda x: 1 if x > 10 else 0)

    
    return df

# Extracting datetime features
def extract_datetime_features(df):
    
    df['receipt_date']=pd.to_datetime(df['receipt_date'],format='%Y-%m-%d')
    df['due_date']=pd.to_datetime(df['due_date'],format="%Y-%m-%d")
    df['weighted_payment_date']=pd.to_datetime(df['weighted_payment_date'],format='%Y-%m-%d')
    
    #Extract due_date features
    def due_date_features(df):
        df['day_of_due_date'] = df['due_date'].dt.day
        df['month_of_due_date'] = df['due_date'].dt.month
        df['year_of_due_date'] = df['due_date'].dt.year
        df['day_of_week'] = df['due_date'].dt.dayofweek
        
        return df
    
    
    df = due_date_features(df)
    
    return df

