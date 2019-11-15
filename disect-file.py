# New Jersey Property Tax Files 
# https://www.state.nj.us/treasury/taxation/lpt/TaxListSearchPublicWebpage.shtml
#

import os
import pandas as pd
import fuzzy
import geocoder as gcode
from datetime import datetime

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))

def get_latlang(street, town, postal_zip):
    return gcode.google('{} {} {}'.format(street, town, postal_zip)).latlng

def cal_score_latlang(street1, street2, town, postal_zip):
    return int(get_latlang(street1, town, postal_zip)== get_latlang(street2, town, postal_zip))                        

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

def load_file(file_nm):
    fwidths = [4,9,9,11,2,2,6,4,8,3,25,15,20,9,20,20,4,4,35,25,25,9,4,6,1,5,10,5,5,1,6,9,9,2,9,9,2,2,1,1,2,1,2,2,3,6,6,12,20,5,4,1,9,9,
               9,3,3,3,3,1,8,1,8,1,8,1,8,4,4,4,3,3,4,4,29,5,4,3,10,1,4,9,9,5,9,9,9,9,9,9,9,9,1,9,9,9]
    columns = ['county_district','block','lot','qualifier','record_id','filler1','transaction_date_mmddyy','transaction_update_no',
               'tax_account_number','property_class','property_location','building_description','land_description','calculated_acreage',
               'addition_lots1','addition_lots2','zoning','tax_map_page_number','owner_name','street_address','city_state','zip_code',
               'number_of_owners','deduction_amount','filler2','bank_code','mortgage_account_number','deed_book','deed_page',
               'sales_price_code','deed_date_mmddyy','sale_price','sale_assessment','sale_sr1a_un_code','social_security_no',
               'school_tax_overage','no_of_dwellings','no_of_commercial_dw','multiple_occupancy','percent_owned_code','rebate_code',
               'delinquent_code','epl_own','epl_use','epl_desc','initial_date_mmddyy','further_date_mmddyy','statute_number',
               'facility_name','building_class_code','year_constructed','assessment_code','land_value','improvement_value',
               'net_value','special_tax_code(1)','special_tax_code(2)','special_tax_code(3)','special_tax_code(4)',
               'exemption_code(1)','exemption_amt(1)','exemption_code(2)','exemption_amt(2)','exemption_code(3)','exemption_amt(3)',
               'exemption_code(4)','exemption_amt(4)','senior_citizens_cnt','veterans_cnt','widows_cnt','surv_spouse_cnt',
               'disabled_cnt','user_field1','user_field2','old_property_id','census_tract','census_block','property_use_code',
               'property_flags','rebate_response_flg','rebate_base_year','rebate_base_yr_tax','rebate_base_yr_net_val','filler3',
               'last_year_tax','current_year_tax','non_municipal_half1','non_municipal_half2','municipal_half1','municipal_half2',
               'non_municipal_half3','municipal_half3','bill_status_flag','estimated_qtr3_tax','prior_yr_net_value',
               'statement_of_state_aid_amt']
    return  pd.read_fwf(file_nm, widths=fwidths, names=columns, na_values=' ', keep_default_na=False)

def get_township(df, municipality_code, municipality_name_state):
    _df = df.query("county_district==@municipality_code and property_class=='2'")
    township_df = _df[['block','lot','qualifier','property_location', 'owner_name','street_address','city_state','zip_code']]
    
    name_df = township_df["owner_name"].str.split(",", n = 1, expand = True)
    township_df["last_name"] = name_df[0]
    township_df["first_name"] = name_df[1]
    township_df.drop(columns =["owner_name"], inplace = True) 

    addr_df = township_df["property_location"].str.split(" ", n = 1, expand = True)
    township_df["street_nbr"] = addr_df[0]
    township_df["street_nm"] = addr_df[1]

    township_df.loc[:,'property_city_state'] = municipality_name_state
    township_df.loc[:,'score_city_state'] = township_df.apply (lambda row: calc_score(row['city_state'],row['property_city_state']), axis=1)

    township_df.loc[:,'possible_rental'] = (township_df['score_city_state']==0)
    #township_df['is_rental'].loc[township_df['is_rental'] == False] = 0
    #township_df['is_rental'].loc[ township_df['is_rental'] == True] = 1

    #township_df.drop(columns =["score_city_state"], inplace = True) 
    #township_df.drop(columns =["property_location"], inplace = True) 
    #township_df.drop(columns =["street_address"], inplace = True) 
    #township_df.drop(columns =["city_state"], inplace = True) 
    #township_df.drop(columns =["zip_code"], inplace = True) 
    return township_df[['last_name', 'first_name','street_nbr','street_nm','property_city_state','possible_rental','block','lot','qualifier']]
    
def get_township_list():
    import configparser
    config = configparser.ConfigParser()
    config_file = os.path.join(SCRIPT_PATH,'township-codes.txt')
    print(f'township list file:{config_file}')    
    config.read(config_file)
    '''
    for section_name in config.sections():
        print('Section:', section_name)
        print('  Options:', config.options(section_name))
        for key, value in config.items(section_name):
            print('  {} = {}'.format(key, value))
        print()
    '''    
    # print(config.get('municipality','1205'))
    # print(type(config.items('municipality')))

    return {int(k):v for k, v in config.items('municipality')}

# ----------------------------------------------------------------------------------------------------------------------------------------
# county_data_file = r'C:\Maru\bhavferi-data\Somerset19.txt' # 
county_data_file = r'C:\Maru\bhavferi-data\Middlesex19.txt'
municipality_code = 1205

towns = get_township_list()
town_name = towns.get(municipality_code)
if town_name is None:
    raise ValueError ('No Town found in lookup') 

print (f'getting data for {municipality_code}-{town_name}...')
print (f'from data file {county_data_file}...')

# -- Actual processing ----------------------
start_time = datetime.now()
print(f'{start_time.isoformat()}: parse file...')
df = load_file(county_data_file)
end_time = datetime.now()
print(f'{end_time.isoformat()}:Recods in file: {df.shape} ({(end_time-start_time).seconds} sec)')# 248263
#print(df.head())
print(f'filter for municipality {municipality_code}-{town_name}')
town_df = get_township(df, f"{municipality_code}", f'{town_name}')
print(town_df.shape)# 248263
print(town_df.head(25))

town_file = f'{town_name.replace(" ","-")}-{municipality_code}-with-block.csv'
town_file = os.path.join('C:\\Maru\\bhavferi-data', town_file)
print(f'data will be exported to {town_file}')
town_df.to_csv(town_file, sep=',', na_rep='', header=True, index=False)
print('data will be exported...')
 
 