import pandas as pd


fwidths = [4,9,9,11,2,2,6,4,8,3,25,15,20,9,20,20,4,4,35,25,25,9,4,6,1,5,10,5,5,1,6,9,9,2,9,9,2,2,1,1,2,1,2,2,3,6,6,12,20,5,4,1,9,9,9,3,3,3,3,1,8,1,8,1,8,1,8,4,4,4,3,3,4,4,29,5,4,3,10,1,4,9,9,5,9,9,9,9,9,9,9,9,1,9,9,9]

columns = ['county_district','block','lot','qualifier','record_id','filler','transaction_date_mmddyy','transaction_update_no','tax_account_number','property_class','property_location','building_description','land_description','calculated_acreage','addition_lots1','addition_lots2','zoning','tax_map_page_number','owner_name','street_address','city_state','zip_code','number_of_owners','deduction_amount','filler','bank_code','mortgage_account_number','deed_book','deed_page','sales_price_code','deed_date_mmddyy','sale_price','sale_assessment','sale_sr1a_un_code','social_security_no','school_tax_overage','no_of_dwellings','no_of_commercial_dw','multiple_occupancy','percent_owned_code','rebate_code','delinquent_code','epl_own','epl_use','epl_desc','initial_date_mmddyy','further_date_mmddyy','statute_number','facility_name','building_class_code','year_constructed','assessment_code','land_value','improvement_value','net_value','special_tax_code(1)','special_tax_code(2)','special_tax_code(3)','special_tax_code(4)','exemption_code(1)','exemption_amt(1)','exemption_code(2)','exemption_amt(2)','exemption_code(3)','exemption_amt(3)','exemption_code(4)','exemption_amt(4)','senior_citizens_cnt','veterans_cnt','widows_cnt','surv_spouse_cnt','disabled_cnt','user_field1','user_field2','old_property_id','census_tract','census_block','property_use_code','property_flags','rebate_response_flg','rebate_base_year','rebate_base_yr_tax','rebate_base_yr_net_val','filler','last_year_tax','current_year_tax','non_municipal_half1','non_municipal_half2','municipal_half1','municipal_half2','non_municipal_half3','municipal_half3','bill_status_flag','estimated_qtr3_tax','prior_yr_net_value','statement_of_state_aid_amt']

'''
file_name = r'C:\FINRA\property_data\test_fixedformatfile.txt'
df = pd.read_fwf(file_name, widths = fwidths,names = columns, na_values=' ',keep_default_na=False)
#print(df)
print(df.shape) #<30M
print(df.head(2))
'''
file_name = r'C:\FINRA\property_data\Middlesex17.txt'
df = pd.read_fwf(file_name, widths = fwidths,names = columns, na_values=' ',keep_default_na=False)
#print(df)
print(df.shape)# 248263
pisc_df = df.query("county_district=='1217' and property_class=='2'")
print(pisc_df.shape) #15028/13545
#print(pisc_df.head(2))
town_nm_df = pisc_df[['city_state','zip_code']].drop_duplicates(subset=['city_state','zip_code'], keep='first', inplace=False)
print(town_nm_df.shape) #535
#print(town_nm_df)
with open(r'C:\FINRA\property_data\city_state_1217.csv','w') as city_state:
    town_nm_df.to_csv(city_state, header=False)

