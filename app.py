import folium
import pandas as pd
from flask import Flask, render_template


def find_top_confirmed(n=15):
    corona_df = pd.read_csv("covid-19-dataset-3.csv")
    by_country = corona_df.groupby('Country_Region').sum()[['Confirmed', 'Deaths', 'Recovered', 'Active']]
    cdf = by_country.nlargest(n, 'Confirmed')[['Confirmed']]
    return cdf


cdf = find_top_confirmed()
pairs = [(country, confirmed) for country, confirmed in zip(cdf.index, cdf['Confirmed'])]

corona_df = pd.read_csv("covid-19-dataset-3.csv")
corona_df = corona_df[['Lat', 'Long_', 'Confirmed']]
corona_df = corona_df.dropna()

m = folium.Map(location=[12.9716, 77.5946],

               zoom_start=4)


def circle_maker(x):
    folium.Circle(location=[x[0], x[1]],
                  radius=float(x[2]),
                  color="green",
                  popup='confirmed cases:{}'.format(x[2])).add_to(m)


corona_df.apply(lambda x: circle_maker(x), axis=1)

html_map = m._repr_html_()


app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html", table=cdf, cmap=html_map, pairs=pairs)


if __name__ == "__main__":
    app.run(debug=True)
