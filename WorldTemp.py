import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import streamlit as st
import urllib.parse
#read csv file
#create DataFrame
df = pd.read_csv("average-monthly-surface-temperature.csv")
continents = {"Europe":["Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands", "Poland", "Portugal", "Romania", "Slovakia", "Slovenia", "Spain", "Sweden"],
              "Asia":["India","China","Indonesia","Pakistan","Bangladesh","Japan","Philippines","Vietnam","Turkey","Iran","Thailand","Myanmar","South Korea","Iraq","Afghanistan","Saudi Arabia","Uzbekistan","Malaysia","Yemen","Nepal","North Korea","Sri Lanka","Kazakhstan","Syria","Cambodia","Jordan","Azerbaijan","United Arab Emirates","Tajikistan"],
              "Africa":["Nigeria","Ethiopia","Egypt","Democratic Republic of the Congo","Tanzania","South Africa","Kenya","Uganda","Sudan","Algeria","Morocco","Angola","Mozambique","Ghana","Madagascar","Cameroon","Côte d'Ivoire","Niger","Burkina Faso","Mali","Malawi","Zambia","Senegal","Chad","Somalia","Zimbabwe","Guinea","Rwanda","Benin"],
              "Oceania":["Australia","Papua New Guinea","New Zealand","Fiji","Solomon Islands","Vanuatu","Samoa","Kiribati","Tonga","Micronesia","Marshall Islands","Palau","Tuvalu","Nauru"],
              "North America":["United States","Mexico","Canada","Guatemala","Cuba","Haiti","Dominican Republic","Honduras","Nicaragua","El Salvador","Costa Rica","Panama","Jamaica","Trinidad and Tobago","Bahamas","Barbados","Saint Lucia","Saint Vincent and the Grenadines","Grenada","Antigua and Barbuda","Saint Kitts and Nevis","Belize"],
              "South America":["Brazil","Colombia","Argentina","Peru","Venezuela","Chile","Ecuador","Bolivia","Paraguay","Uruguay","Guyana","Suriname"]} #dictionary with continents and countries
top_contributors = {}
def wiki_link(country):
    return f"https://en.wikipedia.org/wiki/{urllib.parse.quote(country)}"
country_wiki = {country: wiki_link(country) for continent,countries in continents.items() for country in countries}
for continent in continents.keys():
    df_continent = df[df["Entity"].isin(continents[continent])]
    country_temperature_avg = df_continent.groupby("Entity")["Average surface temperature"].mean().dropna()
    top_3_countries = country_temperature_avg.sort_values(ascending=False).head(3)
    top_contributors[continent] = top_3_countries

# Select the continent
selected_continent = st.selectbox("Select a continent", list(continents.keys()))
  #dropdown to select continent
continent_countries = continents[selected_continent]  #list of countries in selected continent (may not have all countries)
continent_countries.insert(0,"All countries")    #inserting "All countries" at the beginning of the list
selected_country = st.selectbox("Select a country",continent_countries)  #dropdown to select country
if selected_country != "All countries":
  st.markdown(f"Click [here]({country_wiki[selected_country]}) to know more about {selected_country}") #displaying the link to the selected country's wikipedia page
df_continent = df[df["Entity"].isin(continents[selected_continent])] #DataFrame containing data of selected continent
if selected_country == "All countries":
  temperature_avg = df_continent.groupby("year")["Average surface temperature"].mean().dropna()
  title = f"Average surface temperature in {selected_continent}"   #shows plot title as selected continent
else:
  temperature_avg = df[df["Entity"]==selected_country].groupby("year")["Average surface temperature"].mean().dropna()
  title = f"Average surface temperature in {selected_country}"  #shows plot title as selected country
fig, ax = plt.subplots(figsize=(20, 10))
ax.plot(temperature_avg.index, temperature_avg.values, label="Average surface temperature")
ax.set_xticks(temperature_avg.index[::4])
ax.set_title(title) #depending of the selected country or continent show plot and title
ax.set_xlabel("Year")
ax.set_ylabel("Average Temperature")
ax.legend()
st.pyplot(fig) #displaying plot in streamlit app
 
st.header("Diference between maximum temperatures between continents")
max_temperatures_continents = {}

for continent in continents.keys():
  df_continent = df[df["Entity"].isin(continents[continent])]
  max_temperatures_continents[continent] = df_continent.groupby("year")["Average surface temperature"].max()
df_temperature_max = pd.DataFrame(max_temperatures_continents)
df_diference_of_temps = df_temperature_max.max(axis=1) - df_temperature_max.min(axis=1)

fig_diff, ax_diff = plt.subplots(figsize=(20, 10))
ax_diff.bar(df_diference_of_temps.index, df_diference_of_temps.values,color ="red")
ax_diff.set_title("Diference between maximum temperatures between continents")
ax_diff.set_xlabel("Year")
ax_diff.set_ylabel("Diference of temperatures")
ax_diff.set_xticks(df_diference_of_temps.index[::4])
st.pyplot(fig_diff) #displaying plot in streamlit app
st.header("Countries with the highest average temperature in the selected continent")
top_3_countries = top_contributors.get(selected_continent,[])
st.write(top_3_countries) #displaying the countries with the highest average temperature in the selected continent
