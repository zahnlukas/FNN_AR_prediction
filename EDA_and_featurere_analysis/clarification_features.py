from datetime import timedelta

def clarification_features(df, df_clarifications, w):
    df["count_past_clarifications"] = 0
    df["count_dunning_stops"] = 0
    df["avg_clarification_days"] = 0.0
    w_days = w * 30
    
    # Pseudo code
    """
    Count_past_clarifications:
    Count number of clarifications in w months prior receipt date of current invoice.
    Number of clarifications defined as clarifications with created_at in period prior to receipt_date of current invoice.
    Past clarifications are clarifications with created_at in period prior to receipt_date of current invoice.

    
    Count_dunning_stops:
    Count number of dunning stops in w months prior receipt date of current invoice.
    Past clarifications are clarifications with created_at in period prior to receipt_date of current invoice.


    Avg_clarification_days:
    Calculate the average duration of clarifications in w months prior receipt date of current invoice.
    Past clarifications are clarifications with resolved_at in period prior to receipt_date of current invoice.

    Returns:
        _type_:c df with extra columns
    """
    
    customer_date_ranges = df.groupby('customer_id_enc')['receipt_date'].apply(list).to_dict()
    
    clarifications_dict = df_clarifications.groupby('customer_id')[['created_at', "resolved_at", 'triggers_dunning_stop', 'duration']].apply(lambda x: list(x.itertuples(index=False, name=None))).to_dict()
    
    for customer_id_enc, receipt_dates in customer_date_ranges.items():
        current_customer = df[df['customer_id_enc'] == customer_id_enc]['customer_id'].iloc[0]
        
        clarifications = clarifications_dict.get(current_customer, [])
        
        if not clarifications:
            continue
        
        for i, current_date in enumerate(receipt_dates):
            start_date = current_date - timedelta(days=w_days)
            
            count_clarifications = sum(start_date <= clarification_date < current_date for clarification_date, _, _, _  in clarifications)
            
            count_dunning_stops = sum(start_date <= clarification_date < current_date and dunning_stop 
                                      for clarification_date, _, dunning_stop, _ in clarifications)
            
            durations = [duration for _, resolved_at,  _, duration in clarifications if start_date <= resolved_at < current_date]
            avg_clarification_days = sum(durations) / len(durations) if durations else 0.0
            
            df.loc[(df['customer_id_enc'] == customer_id_enc) & (df['receipt_date'] == current_date), 'count_past_clarifications'] = count_clarifications
            df.loc[(df['customer_id_enc'] == customer_id_enc) & (df['receipt_date'] == current_date), 'count_dunning_stops'] = count_dunning_stops
            df.loc[(df['customer_id_enc'] == customer_id_enc) & (df['receipt_date'] == current_date), 'avg_clarification_days'] = avg_clarification_days
    
    return df





def binned_clarification_features(df):
    import numpy as np
    
    df["binary_count_past_clarifications"] = df.apply(lambda row: 0 if row['count_past_clarifications']  == 0.0 else 1 , axis=1)
    df["log_avg_clarification_days"] = np.log(df["avg_clarification_days"] + 1)
    df["binary_dunning_stop"] = df.apply(lambda row: 0 if row['count_dunning_stops']  == 0 else 1 , axis=1)

    
    return df