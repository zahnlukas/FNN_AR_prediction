from datetime import timedelta

def count_past_reminders(df, df_reminders, w):
    df["count_past_reminders"] = 0
    w_days = w * 30
    
    # Precompute date ranges for each customer
    customer_date_ranges = df.groupby('customer_id_enc')['receipt_date'].apply(list).to_dict()
    
    # Precompute reminders for each customer
    reminders_dict = df_reminders.groupby('customer_id')['reminder_date'].apply(list).to_dict()
    
    for customer_id_enc, receipt_dates in customer_date_ranges.items():
        # Get the actual customer_id
        current_customer = df[df['customer_id_enc'] == customer_id_enc]['customer_id'].iloc[0]
        
        # Get reminders for the current customer
        reminders = reminders_dict.get(current_customer, [])
        
        if not reminders:
            continue
        
        for i, current_date in enumerate(receipt_dates):
            start_date = current_date - timedelta(days=w_days)
            
            # Count reminders in the past w months
            count = sum(start_date <= reminder_date < current_date for reminder_date in reminders)
            
            # Update the DataFrame
            df.loc[(df['customer_id_enc'] == customer_id_enc) & (df['receipt_date'] == current_date), 'count_past_reminders'] = count
    
    return df


def average_reminder_stage(df, df_reminders, w):
    df["average_reminder_stage"] = 0.0
    w_days = w * 30
    
    # Precompute date ranges for each customer
    customer_date_ranges = df.groupby('customer_id_enc')['receipt_date'].apply(list).to_dict()
    
    # Create a dictionary for reminders
    reminders_dict = df_reminders.groupby('customer_id').apply(
        lambda x: list(zip(x['reminder_date'], x['reminder_stage']))).to_dict()
    
    
    for customer_id_enc, receipt_dates in customer_date_ranges.items():
        
        # Get the actual customer_id
        current_customer = df[df['customer_id_enc'] == customer_id_enc]['customer_id'].iloc[0]
        
        # Get reminders for the current customer
        reminders = reminders_dict.get(current_customer, [])
        
        if not reminders:
            continue
        
        for i, current_date in enumerate(receipt_dates):
            start_date = current_date - timedelta(days=w_days)
            
            # Filter reminders in the past w months
            past_reminders = [stage for date, stage in reminders if start_date <= date < current_date]
            
            if past_reminders:
                # Calculate the average reminder stage
                average_stage = sum(past_reminders) / len(past_reminders)
            else:
                average_stage = 0.0
            
            # Update the DataFrame
            df.loc[(df['customer_id_enc'] == customer_id_enc) & (df['receipt_date'] == current_date), 'average_reminder_stage'] = average_stage
    
    return df


def reminders_binning(df_reminders):
    
    df_reminders["binary_avg_reminder_stage"] = df_reminders.apply(lambda row: 0 if row['average_reminder_stage']  <= 1 else 1 , axis=1)
    
    df_reminders["binary_reminder_count"] = df_reminders.apply(lambda row: 0 if row['count_past_reminders'] == 0 else 1 , axis=1)
    
    return df_reminders
