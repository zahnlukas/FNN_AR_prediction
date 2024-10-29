# FNN_payment_prediction
Git repository of my Bachelor Thesis - Description of notebooks in repository


### *EDA_and_feature_analysis* folder
- *Data folder*: Creation of artificial dataset to test the code
- *1.2_Country*: Merge Main DF with countries to get country of customer
- *1_Currency*: Get currency of "amount" column of main df and change to euros
- *2_EDA*: Exploratory data analysis; remove outliers and false entries; check distribution of variables
- *3_DF_creator*: Creation of Dataset 1-5 as proposed in the Thesis
- *4_New_Features_Analysis*: Analysis of features proposed in Thesis; contains hiatograms and other plots includd in Thesis (Near_payment_term plot and ratio_outstanding plot)
- *clarification_features*: Functions for clarification features: Count_past_clarifications; Count_dunning_stops; Avg_clarification_days
- *customer_features*: Functions for customer payment behaviour features
- *reminders_features*: Functions for reminder features
- *utils*: preprocessing() function

### *Models*
- *00_Data_split*: Notebook for splitting the data; Comment out features you don't want to use; select dataset number; FIRST STEP BEFORE MODELS
- *01_Model_1*: Select dataset number based on which you want to evaluate; Output: Average MAE for 10 runs with 20 epochs each; Additionally can run on test set with new customers
- *02_Model_2*: Select dataset number based on which you want to evaluate; Output: Average MAE for 5 runs with 20 epochs each; Additionally can run on test set with new customers
- *03_Model_3*: Select dataset number based on which you want to evaluate
- *04_Hyperparameters*: Hyperparameter Tuning of Model
- *05_SHAP_values*:
- *Naive_model*:
- *feature_scaler*: Custome scaling function that scales takes scaling parameters from X_train
