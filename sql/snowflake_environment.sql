create warehouse if not exists REV_FORECASTING_WH
with warehouse_size = 'XSMALL'
auto_suspend = 60
auto_resume = true
initially_suspended = true;

create database if not exists REV_FORECASTING;

create schema if not exists REV_FORECASTING.RAW;
create schema if not exists REV_FORECASTING.ANALYTICS;
create schema if not exists REV_FORECASTING.SANDBOX;

use warehouse REV_FORECASTING_WH;
use database REV_FORECASTING;
use schema RAW;

/* How to get identifier in new Snowflake UI */
select current_account(), current_region();