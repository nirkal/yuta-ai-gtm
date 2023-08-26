import pandas as pd
import re

# Load the dataset
data_path = 'DevOps Copilot Survey 18-08.csv'
data = pd.read_csv(data_path)

# Define patterns for each currency
currency_patterns = {
    'USD': [r'\$', r'dollar', r'dollars', r'usd'],
    'EUR': [r'€', r'euro', r'euros', r'eur'],
    'INR': [r'₹', r'inr', r'rupee', r'rupees'],
    'SEK': [r'sek', r'kr', r'kroner', r'krona'],
    'ZAR': [r'zar', r'rand', r'rands'],
    'GBP': [r'£', r'gbp', r'pound', r'pounds']
}

# Function to interpret the currency for each value
def interpret_currency(value):
    for currency, patterns in currency_patterns.items():
        for pattern in patterns:
            if re.search(pattern, str(value), re.IGNORECASE):
                return str(value) + ' (' + currency + ')'
    return value

# Apply the interpret_currency function to the column
column_name = 'Assume, a DevOps Copilot increases the productivity of a DevOps engineer in your team by 30% on average. What would be the price you are willing to pay, on a monthly subscription basis per engineer? Please indicate the currency (ex. X EUR or Y INR)'
interpreted_willingness_to_pay = data[column_name].apply(interpret_currency)

# Print out each value with its interpreted currency
print(interpreted_willingness_to_pay.to_string())

# Drop NA values from the 'willingness to pay' column
data_cleaned = data.dropna(subset=[column_name])

# 2. Define conversion rates to USD
conversion_rates_to_usd = {
    'INR': 0.013,
    'EUR': 1.18,
    'USD': 1,
    'SEK': 0.12,
    'ZAR': 0.068,
    'GBP': 1.38
}

# 3 & 4. Function to interpret the currency and convert to USD
def convert_to_usd(price):
    # Extract the numeric value and currency from the string
    value = re.search(r'(\d+\.?\d*)', price)
    currency = re.search(r'(\D+)', price)
    
    # Convert the price to USD if possible
    if value and currency:
        value = float(value.group(1))
        currency = currency.group(1).strip().upper()
        if currency in conversion_rates_to_usd:
            return value * conversion_rates_to_usd[currency]
    return price

# Apply the conversion function to the column and store in a new column 'Price_in_USD'
data_cleaned['Price_in_USD'] = data_cleaned[column_name].apply(lambda x: convert_to_usd(x) if isinstance(x, str) else x)

# Print out each value with its interpreted currency
print(data_cleaned[[column_name, 'Price_in_USD']].to_string())

# 5. Filter the data for startups using the correct column name
startup_data = data_cleaned[data_cleaned['How would you categorise the size of your company'] == 'Startup']

# Exclude non-numeric values from the 'Price_in_USD' column for startups
startup_data_numeric = startup_data[pd.to_numeric(startup_data['Price_in_USD'], errors='coerce').notnull()]

# 6. Calculate average and median prices that startups are willing to pay
average_price_startup = startup_data_numeric['Price_in_USD'].mean()
median_price_startup = startup_data_numeric['Price_in_USD'].median()

print(f"Average Price Startups are Willing to Pay: ${average_price_startup:.2f}")
print(f"Median Price Startups are Willing to Pay: ${median_price_startup:.2f}")


## Update the function to also return outliers for a given segment
def analyze_segment_with_outliers(segment_name, is_regulated):
    
    if is_regulated is True:
        segment_data = data_cleaned[data_cleaned['Is your industry highly regulated (ex. Telco, Insurance, Medical etc.)?'] == 'yes']
    else:
        # Filter data for the segment
        segment_data = data_cleaned[data_cleaned['How would you categorise the size of your company'] == segment_name]
    
    # Exclude non-numeric values from the 'Price_in_USD' column for the segment
    segment_data_numeric = segment_data[pd.to_numeric(segment_data['Price_in_USD'], errors='coerce').notnull()]
    
    # Calculate IQR for outlier detection
    Q1_segment = segment_data_numeric['Price_in_USD'].quantile(0.25)
    Q3_segment = segment_data_numeric['Price_in_USD'].quantile(0.75)
    IQR_segment = Q3_segment - Q1_segment

    # Determine bounds for outliers
    lower_bound_segment = Q1_segment - 1.5 * IQR_segment
    upper_bound_segment = Q3_segment + 1.5 * IQR_segment

    # Extract outliers
    outliers_segment = segment_data_numeric[(segment_data_numeric['Price_in_USD'] < lower_bound_segment) | 
                                            (segment_data_numeric['Price_in_USD'] > upper_bound_segment)]
    
    # Exclude outliers for further calculations
    segment_data_without_outliers = segment_data_numeric[(segment_data_numeric['Price_in_USD'] >= lower_bound_segment) & 
                                                         (segment_data_numeric['Price_in_USD'] <= upper_bound_segment)]
    
    # Calculate average and median prices without outliers
    average_price_segment = segment_data_without_outliers['Price_in_USD'].mean()
    median_price_segment = segment_data_without_outliers['Price_in_USD'].median()
    
    # Extract individual features, group by feature, and calculate average price for each feature
    exploded_data_segment = segment_data_without_outliers.assign(features=segment_data_without_outliers["Select all the important features/functions you would expect from a DevOps Copilot."].str.split(',')).explode('features')
    exploded_data_segment['features'] = exploded_data_segment['features'].str.strip()
    average_price_per_feature_segment = exploded_data_segment.groupby('features')['Price_in_USD'].mean().sort_values(ascending=False)
    
    return average_price_segment, median_price_segment, average_price_per_feature_segment, outliers_segment[['Price_in_USD']]

# Analyze Small/Mid-size companies using the correct segment name and print outliers
average_price_small_mid, median_price_small_mid, features_small_mid, outliers_small_mid = analyze_segment_with_outliers('Small or Mid size company', False)

# Analyze Enterprises and print outliers
average_price_enterprise, median_price_enterprise, features_enterprise, outliers_enterprise = analyze_segment_with_outliers('Enterprise', False)

# Analyze Startups and print outliers
average_price_startup, median_price_startup, features_startup, outliers_startup = analyze_segment_with_outliers('Startup', False)

print(average_price_small_mid, median_price_small_mid, features_small_mid, outliers_small_mid, average_price_enterprise, median_price_enterprise, features_enterprise, outliers_enterprise, average_price_startup, median_price_startup, features_startup, outliers_startup)

# Analyze Regulated
average_price_reg, median_price_reg, features_reg, outliers_reg = analyze_segment_with_outliers(None, True)
print(average_price_reg, median_price_reg, features_reg, outliers_reg)
