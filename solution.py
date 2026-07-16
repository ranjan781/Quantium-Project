import pandas as pd

# Read the CSV files
df1 = pd.read_csv("data/daily_sales_data_0.csv")
df2 = pd.read_csv("data/daily_sales_data_1.csv")
df3 = pd.read_csv("data/daily_sales_data_2.csv")

# Combine them
df = pd.concat([df1, df2, df3], ignore_index=True)

# Keep only pink morsel
df = df[df["product"].str.lower() == "pink morsel"]

# Convert price to float
df["price"] = df["price"].replace(r"[\$,]", "", regex=True).astype(float)

# Calculate sales
df["Sales"] = df["quantity"] * df["price"]

# Keep required columns
df = df[["Sales", "date", "region"]]

# Rename columns
df.columns = ["Sales", "Date", "Region"]

# Save output
df.to_csv("formatted_output.csv", index=False)

print("formatted_output.csv has been created successfully!")