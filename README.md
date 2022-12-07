# Domain-Auctions
Access the Domain API to get auction results for support major cities. 

The basis of this project began in Febuary 2022 while looking to purchase a house. 
I soon discovered there were some limitations on the front end searching of the two dominant real estate websites in Australia.

I came across this project by Alex D'Ambra which utilised the Domain API. 
https://medium.com/@alexdambra/how-to-get-aussie-property-price-guides-using-python-the-domain-api-afe871efac96

After reading the Domain API documentation I realised that it would be possible to get the sales results for properties and use this to make more informed decisions about prices. This coincided with the start of the RBA rate rises and increased speculation about residential property prices.

After some further research I started this project to teach myself the foundations of Python and REST API's. 
Several weeks later I had developed this script that allows me to get the auction results for the major cities supported by the Domain API 
and write them to a database which I then hook into via PowreBI/Tableau for visualisation. 

To run this script you will need your own Domain Developer account and client_id and client_secret which can be done here
https://developer.domain.com.au/

An example of the data visualisation below. Colour density indicating median Price, the number indicating number of sales within each Postcode.

![Tableau_example](https://user-images.githubusercontent.com/113073854/206088732-b924e4b1-7cd4-4350-af72-eb5d15a2086e.PNG)


Note: The data gathered from Domain is not complete and there will be instances where the purchases has chosen to withhold the sale price which will result in a _null_ value for Price. The above visualisation is for demonstrative purposes and may differ from other sources. 
