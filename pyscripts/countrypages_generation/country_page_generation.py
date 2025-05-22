"""
This script generate country pages
"""

import pandas as pd
from pathlib import Path
import requests

def get_wikicommons_image_url(image_name):
    image_name = image_name.replace(" ", "_").replace("+", "%2B")
    wikiurl = f"https://en.wikipedia.org/w/api.php?action=query&titles=File:{image_name}&prop=imageinfo&iiprop=url&format=json"
    print("URL =", wikiurl )
    r = requests.get(wikiurl)
    r.raise_for_status()
    print(r)
    r = r.json()
    for key, val in r["query"]["pages"].items():
        return val["imageinfo"][0]["url"]

df_wikidata = pd.read_csv("wikidata_countries_info_formatted.csv", na_filter = False)
wikidata_dict = {row["codeiso2"]: row for row in df_wikidata.to_dict(orient='records')}
print(df_wikidata.columns)

df = pd.read_csv("openinframap_countries_info_brut.csv", na_filter = False)
openinframap_dict = {row["codeiso2"]: row for row in df.to_dict(orient='records')}

print(df.columns)

df = pd.read_csv("powergrid_analysis_countries_info.csv", na_filter = False)
powergrid_dict = {row["codeiso2"]: row for row in df.to_dict(orient='records')}
print(df.columns)

COUNTRY_PAGE_TEMPLATE = "country_page_template.md"

DESTINATION_DIRECTORY = Path(__file__).parent.parent.parent / "docs/countrypages"
MAPS_IMAGES_DIRECTORY = Path(__file__).parent.parent.parent / "docs/images/maps_countries"
print("Destination directory = ", DESTINATION_DIRECTORY)


""" Following lines extract the country list per continent. You can use one of the following dict as a country list"""
#extract_dict = {row["codeiso2"]: row["name"] for row in df_wikidata.to_dict(orient='records') if row["continent"]=="Africa"}
#print(extract_dict)
Africa = {'AO': 'Angola', 'BF': 'Burkina Faso', 'BI': 'Burundi', 'BJ': 'Benin', 'BW': 'Botswana', 'CD': 'Democratic Republic of the Congo', 'CF': 'Central African Republic', 'CG': 'Republic of the Congo', 'CI': 'Ivory Coast', 'CM': 'Cameroon', 'CV': 'Cape Verde', 'DJ': 'Djibouti', 'DZ': 'Algeria', 'EG': 'Egypt', 'ER': 'Eritrea', 'ET': 'Ethiopia', 'GA': 'Gabon', 'GH': 'Ghana', 'GM': 'The Gambia', 'GN': 'Guinea', 'GQ': 'Equatorial Guinea', 'GW': 'Guinea-Bissau', 'KE': 'Kenya', 'KM': 'Comoros', 'LR': 'Liberia', 'LS': 'Lesotho', 'LY': 'Libya', 'MA': 'Morocco', 'MG': 'Madagascar', 'ML': 'Mali', 'MR': 'Mauritania', 'MU': 'Mauritius', 'MW': 'Malawi', 'MZ': 'Mozambique', 'NA': 'Namibia', 'NE': 'Niger', 'NG': 'Nigeria', 'RW': 'Rwanda', 'SC': 'Seychelles', 'SD': 'Sudan', 'SL': 'Sierra Leone', 'SN': 'Senegal', 'SO': 'Somalia', 'SS': 'South Sudan', 'ST': 'São Tomé and Príncipe', 'SZ': 'Eswatini', 'TD': 'Chad', 'TG': 'Togo', 'TN': 'Tunisia', 'TZ': 'Tanzania', 'UG': 'Uganda', 'ZA': 'South Africa', 'ZM': 'Zambia', 'ZW': 'Zimbabwe'}
## SouthAmerica = {'AR': 'Argentina', 'BO': 'Bolivia', 'BR': 'Brazil', 'CL': 'Chile', 'CO': 'Colombia', 'EC': 'Ecuador', 'GY': 'Guyana', 'PA': 'Panama', 'PE': 'Peru', 'PY': 'Paraguay', 'SR': 'Suriname', 'UY': 'Uruguay', 'VE': 'Venezuela'}
SouthAmerica_light = {'AR': 'Argentina', 'BO': 'Bolivia', 'CL': 'Chile', 'CO': 'Colombia', 'EC': 'Ecuador', 'GY': 'Guyana', 'PA': 'Panama', 'PE': 'Peru', 'PY': 'Paraguay', 'SR': 'Suriname', 'UY': 'Uruguay', 'VE': 'Venezuela'}
## Asia = {'AE': 'United Arab Emirates', 'AF': 'Afghanistan', 'AM': 'Armenia', 'AZ': 'Azerbaijan', 'BD': 'Bangladesh', 'BH': 'Bahrain', 'BN': 'Brunei', 'BT': 'Bhutan', 'CN': "People's Republic of China", 'ID': 'Indonesia', 'IL': 'Israel', 'IN': 'India', 'IQ': 'Iraq', 'IR': 'Iran', 'JO': 'Jordan', 'JP': 'Japan', 'KG': 'Kyrgyzstan', 'KH': 'Cambodia', 'KP': 'North Korea', 'KR': 'South Korea', 'KW': 'Kuwait', 'KZ': 'Kazakhstan', 'LA': 'Laos', 'LB': 'Lebanon', 'LK': 'Sri Lanka', 'MM': 'Myanmar', 'MN': 'Mongolia', 'MV': 'Maldives', 'MY': 'Malaysia', 'NP': 'Nepal', 'OM': 'Oman', 'PH': 'Philippines', 'PK': 'Pakistan', 'PS': 'State of Palestine', 'QA': 'Qatar', 'SA': 'Saudi Arabia', 'SG': 'Singapore', 'SY': 'Syria', 'TH': 'Thailand', 'TJ': 'Tajikistan', 'TL': 'Timor-Leste', 'TM': 'Turkmenistan', 'TR': 'Turkey', 'TW': 'Taiwan', 'UZ': 'Uzbekistan', 'VN': 'Vietnam', 'YE': 'Yemen'}
Asia_light = {'AE': 'United Arab Emirates', 'AF': 'Afghanistan', 'AM': 'Armenia', 'AZ': 'Azerbaijan', 'BD': 'Bangladesh', 'BH': 'Bahrain', 'BN': 'Brunei', 'BT': 'Bhutan', 'ID': 'Indonesia', 'IL': 'Israel', 'IQ': 'Iraq', 'IR': 'Iran', 'JO': 'Jordan', 'JP': 'Japan', 'KG': 'Kyrgyzstan', 'KH': 'Cambodia', 'KP': 'North Korea', 'KR': 'South Korea', 'KW': 'Kuwait', 'KZ': 'Kazakhstan', 'LA': 'Laos', 'LB': 'Lebanon', 'LK': 'Sri Lanka', 'MM': 'Myanmar', 'MN': 'Mongolia', 'MV': 'Maldives', 'MY': 'Malaysia', 'NP': 'Nepal', 'OM': 'Oman', 'PH': 'Philippines', 'PK': 'Pakistan', 'PS': 'State of Palestine', 'QA': 'Qatar', 'SA': 'Saudi Arabia', 'SG': 'Singapore', 'SY': 'Syria', 'TH': 'Thailand', 'TJ': 'Tajikistan', 'TL': 'Timor-Leste', 'TM': 'Turkmenistan', 'TR': 'Turkey', 'TW': 'Taiwan', 'UZ': 'Uzbekistan', 'VN': 'Vietnam', 'YE': 'Yemen'}

# No Brazil, China and India in light dict
COUNTRY_LIST = { **Africa, **SouthAmerica_light, **Asia_light }
COUNTRY_LIST = {'DK': 'Danish'}
COUNTRY_LIST = {row["codeiso2"]: row["name"] for row in df_wikidata.to_dict(orient='records')}
SKIP_UNTIL = None # not in use yet

#The following section are conditional, only for countries with map
SECTION_PROGRESS_MAP = """
## Progress map

![Map](../images/maps_countries/{{COUNTRY_CODE}}/high-voltage-network.png){width=90%}
"""

SECTION_GRID_CONNECTIVITY = """
## Grid connectivity overview

Grid connectivity summary (nb of substations x nb of connections) :<br>{{POWER_GRID_CONNECTIVITY}}

![Map](../images/maps_countries/{{COUNTRY_CODE}}/grid-connectivity.png){width=90%}
"""

## Building MD file &

df_collector = []
for country_key in COUNTRY_LIST:
    template_data = {}
    template_data["COUNTRY_CODE"] = country_key

    template_data["COUNTRY_NAME"] = wikidata_dict[country_key]["countryLabel"]
    template_data["COUNTRY_CONTINENT"] = wikidata_dict[country_key]["continent"]
    template_data["COUNTRY_POPULATION"] = wikidata_dict[country_key]["population"]
    template_data["COUNTRY_AREA"] = wikidata_dict[country_key]["area_km2"]
    template_data["COUNTRY_GDP"] = wikidata_dict[country_key]["gdp_bd"]
    template_data["COUNTRY_OSM_REL_ID"] = wikidata_dict[country_key]["osm_rel_id"]
    template_data["COUNTRY_WIKIDATA_ID"] = wikidata_dict[country_key]["osm_rel_id"]
    template_data["COUNTRY_FLAG_IMAGE"] = get_wikicommons_image_url(wikidata_dict[country_key]["flag_image"])
    template_data["COUNTRY_MAP_IMAGE"] = get_wikicommons_image_url(wikidata_dict[country_key]["locator_map"])

    template_data["POWER_LINES_KM"] = openinframap_dict[country_key]["power_line_total_length"]
    template_data["POWER_PLANTS_MW"] = openinframap_dict[country_key]["power_plant_output_mw"]
    template_data["POWER_PLANTS_NB"] = int(openinframap_dict[country_key]["power_plant_count"])

    template_data["POWER_SUBSTATIONS_NB"] = ''
    template_data["POWER_INTERCONNECTIONS_NB"] = ''
    template_data["POWER_GRID_CONNECTIVITY"] = ''
    if powergrid_dict[country_key]["nb_substations"]:
        template_data["POWER_SUBSTATIONS_NB"] = int(float(powergrid_dict[country_key]["nb_substations"]))
        template_data["POWER_INTERCONNECTIONS_NB"] = int(float(powergrid_dict[country_key]["nb_international_connections"]))
        template_data["POWER_GRID_CONNECTIVITY"] = powergrid_dict[country_key]["grid_connectivity"]

    template_data["SECTION_GRID_CONNECTIVITY"] = ""
    template_data["SECTION_PROGRESS_MAP"] = ""
    if Path(MAPS_IMAGES_DIRECTORY / f"{country_key}/high-voltage-network.png").is_file():
        template_data["SECTION_GRID_CONNECTIVITY"] = SECTION_GRID_CONNECTIVITY
        template_data["SECTION_PROGRESS_MAP"] = SECTION_PROGRESS_MAP

    with open(COUNTRY_PAGE_TEMPLATE, 'r', encoding='utf-8') as f:
        contenu = f.read()
        for key, val in template_data.items():
            contenu = contenu.replace(f'{{{{{key}}}}}', str(val))
        for key, val in template_data.items():
            contenu = contenu.replace(f'{{{{{key}}}}}', str(val))

    Path.mkdir(DESTINATION_DIRECTORY, exist_ok=True)
    with open(DESTINATION_DIRECTORY / f"{template_data['COUNTRY_NAME']}.md", 'w', encoding='utf-8') as f:
        f.write(contenu)

    df_collector.append(template_data)

df_collector = pd.DataFrame(df_collector)
## Build
lst_continent = df_collector['COUNTRY_CONTINENT'].unique().tolist()
lst_continent.sort()
for continent in lst_continent:
    print("###", continent, "\n")
    dft = df_collector[df_collector['COUNTRY_CONTINENT']==continent]
    for row in dft.to_dict(orient='records'):
        print(f"![Flag {row['COUNTRY_NAME']}]({row['COUNTRY_FLAG_IMAGE']}){{width=20px}} [{row['COUNTRY_NAME']}](countrypages/{row['COUNTRY_NAME']}.md) - ", end="")
    print("\n")
