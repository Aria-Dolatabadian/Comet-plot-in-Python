import altair as alt
import pandas as pd

# Read the CSV data into a DataFrame
df = pd.read_csv('barley_yield_data.csv')

# Compute delta (difference in yield between years)
df['delta'] = df.groupby(['variety', 'site'])['yield'].diff().fillna(0)

# Create the comet chart
chart = alt.Chart(df).mark_trail().encode(
    alt.X('year:O').title(None),
    alt.Y('variety:N').title('Variety'),
    alt.Size('yield:Q')
        .scale(range=[0, 12])
        .legend(values=[20, 60])
        .title('Barley Yield (bushels/acre)'),
    alt.Color('delta:Q')
        .scale(domainMid=0)
        .title('Yield Delta (%)'),
    alt.Tooltip(['year:O', 'yield:Q']),
    alt.Column('site:N').title('Site')
).transform_pivot(
    "year",
    value="yield",
    groupby=["variety", "site"]
).transform_fold(
    ["1931", "1932", "1933"],
    as_=["year", "yield"]
).transform_calculate(
    calculate="datum['1933'] - datum['1932'] - datum['1931']",
    as_="delta"
).configure_legend(
    orient='bottom',
    direction='horizontal'
).configure_view(
    stroke=None
).properties(
    width=140,   # Set the width of the chart
    height=200   # Set the height of the chart
)

chart.save('chart.html')
