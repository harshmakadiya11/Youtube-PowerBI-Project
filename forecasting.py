import pandas as pd
from prophet import Prophet

subs = pd.read_csv("data/subscriber_timeseries.csv")
forecast_list = []

for name in subs['channel_name'].unique():
    df = subs[subs['channel_name'] == name][['date', 'subscribers']]
    if len(df.dropna()) < 2:
        print(f"⚠️ Skipping '{name}': Not enough data to forecast.")
        continue
    df.columns = ['ds', 'y']
    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)
    forecast['channel_name'] = name
    forecast['days_ahead'] = (forecast['ds'] - pd.to_datetime(df['ds'].max())).dt.days
    forecast['growth_rate'] = forecast['yhat'].diff().fillna(0)
    forecast_list.append(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper', 'channel_name', 'days_ahead', 'growth_rate']])

if forecast_list:
    final = pd.concat(forecast_list)
    final.columns = ['date', 'predicted_subscribers', 'lower_bound', 'upper_bound', 'channel_name', 'days_ahead', 'growth_rate']
    final.to_csv("data/forecasted_subs.csv", index=False)
    print("✅ Forecasting complete.")
else:
    print("⚠️ No channels had enough data to generate forecasts.")
