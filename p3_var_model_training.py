
from statsmodels.tsa.api import VAR
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

from p3_var_data_preparation import var_df_filled_nas
from p2_data_validation import merge_data_one_ticker, column_names

# TODO this needs an overhaul as we don't do the nested loop anymore

def fit_VAR(df, train_end_date, test_start_date, test_end_date, cols, order, start_date, potential_columns=column_names):
    
    df.index = pd.to_datetime(df.index)
    start_date = pd.Timestamp(start_date)
    train_end_date = pd.Timestamp(train_end_date)

    # Split data into train and validation sets
    train_data = df.loc[start_date:train_end_date]
    test_data = df.loc[test_start_date:test_end_date]

    # TODO before fitting, we need to normalize the data as many columns are not stationery
    
    # Fit VAR model
    model = VAR(train_data[potential_columns[:cols]])
    model_fit = model.fit(order)

    # Forecast using the trained model
    forecast_array_test_set = model_fit.forecast(model_fit.endog, steps=len(test_data))

    # Convert the forecast array to a pandas DataFrame
    forecast_df_test_set = pd.DataFrame(forecast_array_test_set, columns=potential_columns[:cols], index=test_data.index)

    forecast_df_test_set = forecast_df_test_set["close"]
    
    # Replace values less than 0 with 0 (prices can't be negative)
    forecast_df_test_set[forecast_df_test_set < 0] = 0

    return {
        'model_fit': model_fit,
        'forecast_test_set': forecast_df_test_set,
        'test_data': test_data
    }

def forecast_VAR(df, cols, order, start_date, potential_columns=column_names):
    df.index = pd.to_datetime(df.index)

    # Fit VAR model
    model = VAR(df[potential_columns[:cols]])
    model_fit = model.fit(order)

    # Forecast using the trained model
    forecast_array_beyond_test_set = model_fit.forecast(model_fit.endog, steps=30)

    # Convert the forecast array to a pandas DataFrame
    forecast_array_beyond_test_set = pd.DataFrame(forecast_array_beyond_test_set, columns=potential_columns[:cols])
    
    # Replace values less than 0 with 0 (prices can't be negative)
    forecast_array_beyond_test_set[forecast_array_beyond_test_set < 0] = 0

    # Array of dates starting from tomorrow
    dates = pd.date_range(start=datetime.today().date() + timedelta(days=1), periods=30)

    # Convert to DataFrame
    df = pd.DataFrame({'Date': dates, 'Value': forecast_array_beyond_test_set["close"]})

    return df



if __name__ == "__main__":

    # configure test and train periods
    test_duration = 60  # change for longer/ shorter test periods (days)
    test_start_date = datetime.strptime('2023-06-10', "%Y-%m-%d") # start of test period
    test_end_date = test_start_date + timedelta(days=test_duration) # end of test period
    train_end_date = test_start_date - timedelta(days=1)

    ticker = "BTC-USD"
    df = merge_data_one_ticker(ticker)
    df = var_df_filled_nas(df)

    cols = len(column_names) + 1
    order = 11 # best order value calculated previously
    start_date = datetime.strptime("2022-01-31", "%Y-%m-%d") # calculated as best start date

    # for now I consider all columns
    dict_fit_VAR_output = fit_VAR(df, train_end_date, test_start_date, test_end_date,
                                  cols, order, start_date, column_names)

    print(dict_fit_VAR_output["forecast_test_set"])

    forecast_array_beyond_test_set = forecast_VAR(df, cols, order, start_date, potential_columns=column_names)
    print(forecast_array_beyond_test_set)

