from urllib.request import urlopen
import plotly.express as px
import pandas as pd
import json

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

df_2020 = pd.read_csv('data/2020_US_County_Level_Presidential_Results.csv')
df_2020['county_fips'] = df_2020['county_fips'].astype(str)
df_2020['county_fips'] = df_2020['county_fips'].str.rjust(5, '0')


df_2024 = pd.read_csv('data/2024_US_County_Level_Presidential_Results.csv')
df_2024['county_fips'] = df_2024['county_fips'].astype(str)
df_2024['county_fips'] = df_2024['county_fips'].str.rjust(5, '0')

df = pd.merge(df_2020, df_2024, on='county_fips', suffixes=('_2020', '_2024'))
df['per_point_diff'] = ((df['per_dem_2024'] - df['per_dem_2020']) / df['per_dem_2020']) * -100

fig = px.choropleth(df, geojson=counties, locations='county_fips', color='per_point_diff',
                           color_continuous_scale="Bluered",
                            range_color=(-10, 10),
                            hover_name="county_name_2020",
                           scope="usa",
                           labels={'per_point_diff':'Percent Shift in Republican Vote'},
                           title='2024 Presidential Election: Change in Republican Vote Share by County (vs 2020)'
                          )
fig.show()