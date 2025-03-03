import pandas as pd 


#* loading csv files

amazon_sales = pd.read_csv("./Data/Amazon Sale Report.csv")
cloud_warehouse = pd.read_csv("./Data/Cloud Warehouse Compersion Chart.csv")
expenses = pd.read_csv("./Data/Expense IIGF.csv")
international_sales = pd.read_csv("./Data/International sale Report.csv")
may_2022 = pd.read_csv("./Data/International sale Report.csv")
pl_march_2021 = pd.read_csv("./Data/P  L March 2021.csv")
sales_report = pd.read_csv("./Data/Sale Report.csv")

# print(amazon_sales.head())
# print(cloud_warehouse.head())
# print(expenses.head())
# print(international_sales.head())
# print(may_2022.head())
# print(pl_march_2021.head())
# print(sales_report.head())



#* creating the dim_data table extracting from all csv dataset that contains date fields
date_frames = [amazon_sales, international_sales, may_2022, sales_report]

for df in date_frames:
    
    if "Date"  in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])


all_dates = pd.concat([df[["Date"]] for df in date_frames if "Date" in df.columns]).drop_duplicates()
#print(all_dates.head())
dim_date = all_dates.copy()

dim_date["date_id"] = dim_date["Date"].dt.strftime("%Y%m%d").astype(int)
dim_date["year"] = dim_date["Date"].dt.year
dim_date["month"] = dim_date["Date"].dt.month
dim_date["day"] = dim_date["Date"].dt.day
dim_date["quarter"] = dim_date["Date"].dt.to_period("Q").astype(str)
#dim_date["Weekday"] = dim_date["Date"].dt.day_name()

dim_date = dim_date[["date_id", "Date", "year", "month", "day", "quarter"]]

print(dim_date.head(10))

#* will continue rest of the dim_tables :) 









