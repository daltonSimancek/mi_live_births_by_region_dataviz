from bs4 import BeautifulSoup
import urllib2
import pandas as pd
from collections import defaultdict
import csv

#################################################################################
# Create a variable with the URL to this tutorial
mdch_url = 'http://www.mdch.state.mi.us/pha/osr/abortion/pregbyco.asp'

# Scrape the HTML at the url
response = urllib2.urlopen(mdch_url)

# Turn the HTML into a Beautiful Soup object
soup = BeautifulSoup(response.read().decode('utf-8'), "html.parser")

# Create two lists to hold each set of variables
births_dict_list = []

# Parse the table section of the html file
table = soup.find('table')
rows = table.find_all('tr')

#Prase each row of the table
for row in rows[1:]:

    col = row.find_all('td')

    # if row is valid, add values to the variable lists
    county_name = col[0].string.strip().encode('utf-8')
    if len(county_name) > 0:

        try:
            live_births = int(col[2].string.strip().replace(',', '').encode('utf-8'))

        except:
            live_births = 0

        new_dict = {
            'county_name':county_name,
            'live_births':live_births
        }

        births_dict_list.append(new_dict)


###############################################################
census_url = 'http://www2.census.gov/geo/docs/reference/codes/files/st26_mi_cou.txt'
fips_codes = list(urllib2.urlopen(census_url))

fips_dict_list = []

for line in fips_codes:
    line = line.split(",")

    try:
        fips_code = int(line[1] + line[2])
    except:
        fips_code = 0

    try:
        county_name = line[3].replace(" County","")
    except:
        county_name = ""

    new_dict = {
        'county_name': county_name,
        'fips_code': fips_code
                }

    fips_dict_list.append(new_dict)

#############################################################

d = defaultdict(dict)
for l in (fips_dict_list, births_dict_list):  #for each of these two lists
    for elem in l:                              # for each dictionary in list
        d[elem['county_name']].update(elem)         # Update this dictionary on county_name key
mi_county_birth_data = d.values()


# Fill in missing fips_code fields with 0
for dictionary in mi_county_birth_data:
    if "fips_code" not in dictionary:
        dictionary['fips_code'] = 0

mi_county_birth_data_FINAL = sorted(mi_county_birth_data, key=lambda k: k['county_name'])
#############################################################

keys = mi_county_birth_data_FINAL[0].keys()
with open('mi_county_births_2014.csv', 'wb') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(mi_county_birth_data_FINAL)












#columns = {'county': county, 'live_births': live_births}




#Convert to dataframe
#df = pd.DataFrame(columns)

#df.to_csv("mi_county_births_2014.csv", sep=',', encoding='utf-8')
"""
svg = open('counties.svg', 'r').read()
soup_svg = BeautifulSoup(svg, selfClosingTags=['defs','sodipodi:namedview'])
paths = soup_svg.findAll('path')
print paths

map_colors = ['#edf8fb', '#b2e2e2','#66c2a4','#2ca25f', '#006d2c']

# County style
path_style = 'font-size:12px;fill-rule:nonzero;stroke:#FFFFFF;stroke-opacity:1;
stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt;
marker-start:none;stroke-linejoin:bevel;fill:'

# Color the counties based on unemployment rate
for p in paths:

    if p['id'] not in ["State_Lines", "separator"]:
        try:
            rate = unemployment[p['id']]
        except:
            continue


        if rate > 10:
            color_class = 5
        elif rate > 8:
            color_class = 4
        elif rate > 6:
            color_class = 3
        elif rate > 4:
            color_class = 2
        elif rate > 2:
            color_class = 1
        else:
            color_class = 0


        color = colors[color_class]
        p['style'] = path_style + color

print soup.prettify()
"""
