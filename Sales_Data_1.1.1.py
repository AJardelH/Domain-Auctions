import requests
import pandas as pd
import sqlite3

# set up API credential variables
# generate client id and secret via registration at Domain API website
client_id = 'client_id'
client_secret = 'client_secret'
auth_url = 'https://auth.domain.com.au/v1/connect/token'
cities_list = ['Melbourne','Sydney','Canberra','Brisbane','Adelaide']
conn = sqlite3.connect('Auction_Results.db') #db file
c = conn.cursor()

#generate table based on Domain API Schema
c.execute('''CREATE TABLE if not exists TempTable (
    auctionDate string,
    id int,
    propertyDetailsUrl string,
    price int,
    result string,
    unitNumber string,
    streetNumber string,
    streetName string,
    streetType string,
    suburb string,
    postcode string,
    state string,
    propertyType string,
    bedrooms int,
    bathrooms int,
    carspaces int,  
    agencyId int,
    agencyName string,
    agent string,
    agencyProfilePageUrl string,
    latitude real, 
    longitude real
    )''')

c.execute('''CREATE TABLE if not exists AuctionResults (
    auctionDate string,
    id int,
    propertyDetailsUrl string,
    price int,
    result string,
    unitNumber string,
    streetNumber string,
    streetName string,
    streetType string,
    suburb string,
    postcode string,
    state string,
    propertyType string,
    bedrooms int,
    bathrooms int,
    carspaces int,  
    agencyId int,
    agencyName string,
    agent string,
    agencyProfilePageUrl string,
    latitude real, 
    longitude real
    )''')

def authorization():
     global token
     global auth_headers
     get_auth = requests.post(auth_url, data = {
     'client_id':client_id,
     'client_secret':client_secret,
     'grant_type':'client_credentials',
     'scope':'api_salesresults_read',
     'Content-Type':'text/json'
     })
     token=get_auth.json()
     access_token=token['access_token']
     auth_headers = {'Authorization':'Bearer '+access_token,
            'scope':'api_salesresults_read'
            }
    
def get_date():
    '''Gets auction date data from domain api
    creates global parameter auction_date to be used in get_sales_temp
    to append to dataframe'''
    global auction_date
    date_url = 'https://api.domain.com.au/v1/salesResults/_head'
    d = requests.get(date_url, headers= auth_headers)
    date_response = d.json()
    auction_date = date_response['auctionedDate']

def get_sales_temp():
    '''gets sales results from domain api via f string with cities parameter
    normalises the json response to un-nest latitude and longitude
    replaces the prefix geoLocation from lat and lon columns 
    appends global auctionDate to dataframe
    inserts dataframe into TempTable'''

    end_url = f'https://api.domain.com.au/v1/salesResults/{cities}/listings'
    r = requests.get(end_url, headers= auth_headers)  
    sales_response = r.json()
    df = pd.json_normalize(sales_response)
    df = df[df.id != 0]
    df.columns = df.columns.str.replace('geoLocation.','', regex=False)
    df['auctionDate'] = auction_date
    df.to_sql('TempTable', conn, if_exists='append', index=False)
    index = df.index
    number_of_rows = len(index)
    print(f'{number_of_rows} temp records inserted for {cities}')
     
def temp_sales_to_perm():
    '''This function transfers records from the temp table to the perm table
    where the column id does not exist in the perm table
    Drops the temp table after completion'''

    c.executescript('''
    INSERT INTO AuctionResults 
    SELECT * FROM TempTable
    WHERE NOT EXISTS (SELECT * FROM AuctionResults
        WHERE TempTable.id = AuctionResults.id
        AND TempTable.auctionDate = AuctionResults.auctionDate);
    DROP TABLE TempTable;''')
 
authorization()
get_date()

#iterate over available cities 
for i in cities_list:
    cities = i
    get_sales_temp()
   
temp_sales_to_perm()
