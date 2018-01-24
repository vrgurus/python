import pandas as pd
import fuzzy

def calc_soundex(val):
    return fuzzy.Soundex(4)(val)

def calc_dmetaphone(val):
    return fuzzy.DMetaphone()(val)

def calc_nysiss(val):
    return fuzzy.nysiis(val)

def calc_score(val1, val2):
    sndx = int(calc_soundex(val1)== calc_soundex(val2))
    dmeta = int(calc_dmetaphone(val1) == calc_dmetaphone(val2))
    nysiis = int(calc_nysiss(val1) == calc_nysiss(val2))
    return (sndx + dmeta + nysiis)


def calc_match(val):
    sndx = fuzzy.Soundex(4)
    dmeta = fuzzy.DMetaphone()
    return calc_soundex(val), calc_dmetaphone(val), calc_nysiss(val)

def get_street_nbr(val):
    return val[:val.find(' ')]

def get_street_nm(val):
    return val[val.find(' ')+1:]

fwidths = [4,9,9,11,2,2,6,4,8,3,25,15,20,9,20,20,4,4,35,25,25,9,4,6,1,5,10,5,5,1,6,9,9,2,9,9,2,2,1,1,2,1,2,2,3,6,6,12,20,5,4,1,9,9,9,3,3,3,3,1,8,1,8,1,8,1,8,4,4,4,3,3,4,4,29,5,4,3,10,1,4,9,9,5,9,9,9,9,9,9,9,9,1,9,9,9]

columns = ['county_district','block','lot','qualifier','record_id','filler1','transaction_date_mmddyy','transaction_update_no','tax_account_number','property_class','property_location','building_description','land_description','calculated_acreage','addition_lots1','addition_lots2','zoning','tax_map_page_number','owner_name','street_address','city_state','zip_code','number_of_owners','deduction_amount','filler2','bank_code','mortgage_account_number','deed_book','deed_page','sales_price_code','deed_date_mmddyy','sale_price','sale_assessment','sale_sr1a_un_code','social_security_no','school_tax_overage','no_of_dwellings','no_of_commercial_dw','multiple_occupancy','percent_owned_code','rebate_code','delinquent_code','epl_own','epl_use','epl_desc','initial_date_mmddyy','further_date_mmddyy','statute_number','facility_name','building_class_code','year_constructed','assessment_code','land_value','improvement_value','net_value','special_tax_code(1)','special_tax_code(2)','special_tax_code(3)','special_tax_code(4)','exemption_code(1)','exemption_amt(1)','exemption_code(2)','exemption_amt(2)','exemption_code(3)','exemption_amt(3)','exemption_code(4)','exemption_amt(4)','senior_citizens_cnt','veterans_cnt','widows_cnt','surv_spouse_cnt','disabled_cnt','user_field1','user_field2','old_property_id','census_tract','census_block','property_use_code','property_flags','rebate_response_flg','rebate_base_year','rebate_base_yr_tax','rebate_base_yr_net_val','filler3','last_year_tax','current_year_tax','non_municipal_half1','non_municipal_half2','municipal_half1','municipal_half2','non_municipal_half3','municipal_half3','bill_status_flag','estimated_qtr3_tax','prior_yr_net_value','statement_of_state_aid_amt']

file_name = r'C:\Maru\sw\test-file.txt'
file_name = r'C:\Maru\sw\Middlesex17.txt'
df = pd.read_fwf(file_name, widths = fwidths,names = columns, na_values=' ',keep_default_na=False)
#print(df.head(2))
print(df.shape)# 248263
pisc_df = df.query("county_district=='1217' and property_class=='2'")
print('pisc_df.shape:{}'.format(pisc_df.shape)) #15028/13545
#print(pisc_df.head(2))
town_nm_df = pisc_df[['city_state','zip_code']].drop_duplicates(subset=['city_state','zip_code'], keep='first', inplace=False)
print(town_nm_df.shape) #535
#print(town_nm_df)

#with open(r'C:\Maru\sw\city_state_1217.csv','w') as city_state:
#    town_nm_df.to_csv(city_state, header=False)

pisc_homes = pisc_df[['property_location', 'owner_name','street_address','city_state','zip_code']]
pisc_homes.loc[:,'property_city_state'] = 'PISCATAWAY, NJ'
pisc_homes.loc[:,'score_city_state'] = pisc_homes.apply (lambda row: calc_score(row['city_state'],row['property_city_state']), axis=1)
pisc_homes.loc[:,'score_street'] = pisc_homes.apply (lambda row: calc_score(row['property_location'],row['street_address']), axis=1)
print('pisc_homes.shape:{}'.format(pisc_homes.shape))
#print(pisc_homes.head(2))
#print(pisc_homes)
pisc_owner =  pisc_homes.query("score_city_state!=0")
print('pisc_owner.shape:{}'.format(pisc_owner.shape))
pisc_rental = pisc_homes.query("score_city_state==0")
print('pisc_rental.shape:{}'.format(pisc_rental.shape))


pisc_owner.to_csv(r'C:\Maru\sw\pisc_owner.csv', sep='|', na_rep='', header=True, index=False)
pisc_rental.to_csv(r'C:\Maru\sw\pisc_rental.csv', sep='|', na_rep='', header=True, index=False)


#-------------------------------------------------------------------
edison_df = df.query("county_district=='1205' and property_class=='2'")
print('edison_df.shape:{}'.format(edison_df.shape)) #15028/13545
#print(edison_df.head(2))
#town_nm_df = edison_df[['city_state','zip_code']].drop_duplicates(subset=['city_state','zip_code'], keep='first', inplace=False)
#print(town_nm_df.shape) #779
#print(town_nm_df)

#with open(r'C:\Maru\sw\city_state_1217.csv','w') as city_state:
#    town_nm_df.to_csv(city_state, header=False)

edison_homes = edison_df[['property_location', 'owner_name','street_address','city_state','zip_code']]
#edison_homes.loc[:,'property_city_state'] = 'EDISON, NJ'
#edison_homes.loc[:,'property_street#'] = edison_homes.apply(lambda row: get_street_nbr(row['property_location']), axis=1)
#edison_homes.loc[:,'property_street_nm'] = edison_homes.apply(lambda row: get_street_nm(row['property_location']), axis=1)
edison_homes.loc[:,'score_city_state'] = edison_homes.apply (lambda row: calc_score(row['city_state'],'EDISON, NJ'), axis=1)
edison_homes.loc[:,'score_street'] = edison_homes.apply (lambda row: calc_score(row['property_location'],row['street_address']), axis=1)
edison_homes.loc[:,'score_street_nm'] = edison_homes.apply (lambda row: calc_score(get_street_nm(row['property_location']),get_street_nm(row['street_address'])), axis=1)
print('edison_homes.shape:{}'.format(edison_homes.shape)) #25436
#print(edison_homes.head(2))
#print(edison_homes)
edison_owner =  edison_homes.query("score_city_state!=0") #23313
print('edison_owner.shape:{}'.format(edison_owner.shape))
edison_rental = edison_homes.query("score_city_state==0") #2123
print('edison_rental.shape:{}'.format(edison_rental.shape))


edison_owner.to_csv(r'C:\Maru\sw\edison_owner.csv', sep='|', na_rep='', header=True, index=False)
edison_rental.to_csv(r'C:\Maru\sw\edison_rental.csv', sep='|', na_rep='', header=True, index=False)
