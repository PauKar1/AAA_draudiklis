import pandas as pd

file_path = 'C:/Users/pauli/PycharmProjects/AAA_draudiklis/app/management/commands/cont.csv'
data = pd.read_csv(file_path, encoding='latin1')

color_to_risk_level = {
    'green': 'Low',
    'yellow': 'Medium',
    'orange': 'High',
    'red': 'Very High',
    'black': 'Extreme'
}

# colors based on https://keliauk.urm.lt/ map
country_colors = {
    "Afghanistan": "red",
    "Albania": "yellow",
    "Algeria": "orange",
    "Andorra": "green",
    "Angola": "red",
    "Argentina": "yellow",
    "Armenia": "yellow",
    "Australia": "green",
    "Austria": "green",
    "Azerbaijan": "orange",
    "Bahamas": "yellow",
    "Bahrain": "yellow",
    "Bangladesh": "orange",
    "Barbados": "green",
    "Belarus": "red",
    "Belgium": "green",
    "Belize": "yellow",
    "Benin": "orange",
    "Bhutan": "yellow",
    "Bolivia": "yellow",
    "Bosnia and Herzegovina": "yellow",
    "Botswana": "yellow",
    "Brazil": "orange",
    "Brunei": "yellow",
    "Bulgaria": "yellow",
    "Burkina Faso": "red",
    "Burundi": "red",
    "Cabo Verde": "yellow",
    "Cambodia": "yellow",
    "Cameroon": "orange",
    "Canada": "green",
    "Central African Republic": "red",
    "Chad": "red",
    "Chile": "yellow",
    "China": "orange",
    "Colombia": "orange",
    "Comoros": "orange",
    "Congo, Democratic Republic of the": "red",
    "Congo, Republic of the": "orange",
    "Costa Rica": "yellow",
    "Croatia": "green",
    "Cuba": "yellow",
    "Cyprus": "green",
    "Czech Republic": "green",
    "Denmark": "green",
    "Djibouti": "orange",
    "Dominica": "green",
    "Dominican Republic": "yellow",
    "East Timor (Timor-Leste)": "orange",
    "Ecuador": "yellow",
    "Egypt": "orange",
    "El Salvador": "orange",
    "Equatorial Guinea": "orange",
    "Eritrea": "red",
    "Estonia": "green",
    "Eswatini": "yellow",
    "Ethiopia": "red",
    "Fiji": "yellow",
    "Finland": "green",
    "France": "green",
    "Gabon": "yellow",
    "Gambia": "yellow",
    "Georgia": "yellow",
    "Germany": "green",
    "Ghana": "yellow",
    "Greece": "green",
    "Grenada": "green",
    "Guatemala": "orange",
    "Guinea": "orange",
    "Guinea-Bissau": "orange",
    "Guyana": "yellow",
    "Haiti": "red",
    "Honduras": "orange",
    "Hungary": "green",
    "Iceland": "green",
    "India": "orange",
    "Indonesia": "yellow",
    "Iran": "red",
    "Iraq": "red",
    "Ireland": "green",
    "Israel": "orange",
    "Italy": "green",
    "Ivory Coast": "orange",
    "Jamaica": "yellow",
    "Japan": "green",
    "Jordan": "yellow",
    "Kazakhstan": "yellow",
    "Kenya": "orange",
    "Kiribati": "yellow",
    "Korea, North": "red",
    "Korea, South": "green",
    "Kosovo": "yellow",
    "Kuwait": "yellow",
    "Kyrgyzstan": "orange",
    "Laos": "yellow",
    "Latvia": "green",
    "Lebanon": "red",
    "Lesotho": "yellow",
    "Liberia": "orange",
    "Libya": "red",
    "Liechtenstein": "green",
    "Lithuania": "green",
    "Luxembourg": "green",
    "Madagascar": "yellow",
    "Malawi": "yellow",
    "Malaysia": "yellow",
    "Maldives": "yellow",
    "Mali": "red",
    "Malta": "green",
    "Marshall Islands": "yellow",
    "Mauritania": "orange",
    "Mauritius": "green",
    "Mexico": "orange",
    "Micronesia": "yellow",
    "Moldova": "yellow",
    "Monaco": "green",
    "Mongolia": "yellow",
    "Montenegro": "yellow",
    "Morocco": "yellow",
    "Mozambique": "orange",
    "Myanmar": "red",
    "Namibia": "yellow",
    "Nauru": "yellow",
    "Nepal": "yellow",
    "Netherlands": "green",
    "New Zealand": "green",
    "Nicaragua": "orange",
    "Niger": "orange",
    "Nigeria": "red",
    "North Macedonia": "yellow",
    "Norway": "green",
    "Oman": "yellow",
    "Pakistan": "red",
    "Palau": "yellow",
    "Palestine": "orange",
    "Panama": "yellow",
    "Papua New Guinea": "orange",
    "Paraguay": "yellow",
    "Peru": "orange",
    "Philippines": "orange",
    "Poland": "green",
    "Portugal": "green",
    "Qatar": "yellow",
    "Romania": "yellow",
    "Russia": "red",
    "Rwanda": "yellow",
    "Saint Kitts and Nevis": "green",
    "Saint Lucia": "green",
    "Saint Vincent and the Grenadines": "green",
    "Samoa": "yellow",
    "San Marino": "green",
    "Sao Tome and Principe": "yellow",
    "Saudi Arabia": "yellow",
    "Senegal": "yellow",
    "Serbia": "yellow",
    "Seychelles": "green",
    "Sierra Leone": "orange",
    "Singapore": "green",
    "Slovakia": "green",
    "Slovenia": "green",
    "Solomon Islands": "yellow",
    "Somalia": "red",
    "South Africa": "orange",
    "South Sudan": "red",
    "Spain": "green",
    "Sri Lanka": "yellow",
    "Sudan": "red",
    "Suriname": "yellow",
    "Sweden": "green",
    "Switzerland": "green",
    "Syria": "red",
    "Taiwan": "green",
    "Tajikistan": "orange",
    "Tanzania": "yellow",
    "Thailand": "yellow",
    "Togo": "orange",
    "Tonga": "yellow",
    "Trinidad and Tobago": "yellow",
    "Tunisia": "orange",
    "Turkey": "yellow",
    "Turkmenistan": "orange",
    "Tuvalu": "yellow",
    "Uganda": "yellow",
    "Ukraine": "red",
    "United Arab Emirates": "green",
    "United Kingdom": "green",
    "United States": "green",
    "Uruguay": "green",
    "Uzbekistan": "yellow",
    "Vanuatu": "yellow",
    "Vatican City (Holy See)": "green",
    "Venezuela": "red",
    "Vietnam": "yellow",
    "Yemen": "red",
    "Zambia": "yellow",
    "Zimbabwe": "orange"
}

data['Risk'] = data['name'].map(lambda x: color_to_risk_level.get(country_colors.get(x, 'green'), 'Unknown'))
output_file_path = 'C:/Users/pauli/PycharmProjects/AAA_draudiklis/app/management/commands/updated_cont.csv'
data.to_csv(output_file_path, index=False)
data.head()

