
## When Loading data into Snowflake
pip show snowflake-connector-python

## Double check pandas installed
pip install pandas
pip show pandas

select *
from REV_FORECASTING.RAW.accounts_raw
limit 10;

write_pandas() created tables as quoted lowercase identifiers