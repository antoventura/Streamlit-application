import streamlit as st
import pandas as pd
import geopandas as gpd
import geoplot as gplt
import geoplot.crs as gcrs
import mapclassify as mc
import numpy as np
import matplotlib.pyplot as plt
import os

from typing import Tuple

@st.cache_data
def load_files() -> Tuple[gpd.GeoDataFrame, pd.DataFrame]:
    """load dataframes"""
    rioni = gpd.read_file(filename='Data/Roma_ZU.shp').to_crs(epsg=3857)
    
    path = os.path.join(os.getcwd(), "Data/rome_houses_5000_sample.xlsx")
    metro = pd.read_excel(path)
    df = metro[metro["CITTA"] == "Roma"]
    
    return rioni, df

@st.cache_data
def preprocess_data(df: pd.DataFrame) -> gpd.GeoDataFrame:
    houses_df = df.dropna(subset=['LATITUDINE', 'LONGITUDINE', 'PREZZO'])

    # Convert the DataFrame to a GeoDataFrame
    geometry = gpd.points_from_xy(houses_df.LONGITUDINE, houses_df.LATITUDINE)
    houses_gdf = gpd.GeoDataFrame(houses_df, geometry=geometry)
    houses_gdf["geometry"] = houses_gdf["geometry"].set_crs(epsg=4326, inplace=True).to_crs(epsg=3857)
    
    return houses_gdf

def plot_house_prices(houses_gdf: gpd.GeoDataFrame, rioni: gpd.GeoDataFrame, min_price: float, max_price: float):
    fig, ax = plt.subplots(figsize=(15, 15))
    
    rioni.plot(ax=ax, color='white', edgecolor='blue', alpha=0.5)
    
    filtered_houses = houses_gdf[(houses_gdf["PREZZO"] >= min_price) & (houses_gdf["PREZZO"] <= max_price)]
    
    scatter = ax.scatter(
        filtered_houses.geometry.x,
        filtered_houses.geometry.y,
        c=filtered_houses["PREZZO"],
        s=2,
        cmap='icefire',
        alpha=0.7
    )
    
    plt.colorbar(scatter, label='Price (€)', format='%.0f')
    
    ax.set_axis_off()
    
    xlim = (houses_gdf.total_bounds[0]*0.99, houses_gdf.total_bounds[2]*1.01)
    ylim = (houses_gdf.total_bounds[1]*0.999, houses_gdf.total_bounds[3]*1.001)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    
    return fig

def main():
    st.title("Rome House Prices Map")
    
    rioni, df = load_files()
    houses_gdf = preprocess_data(df)
    
    # Create a layout with two columns
    col1, col2 = st.columns([3, 1])
    
    with col2:
        st.subheader("Price Range Filter")
        min_price = houses_gdf["PREZZO"].min()
        max_price = houses_gdf["PREZZO"].max()
        price_range = st.slider(
            "Select Price Range",
            min_value=float(min_price),
            max_value=float(max_price),
            value=(float(min_price), float(max_price)),
            step=10000.0,
            format="€%.0f"
        )
    
    with col1:
        fig = plot_house_prices(houses_gdf, rioni, price_range[0], price_range[1])
        st.pyplot(fig)
    
    st.write(f"Showing houses priced between €{price_range[0]:,.0f} and €{price_range[1]:,.0f}")
    st.write(f"Number of houses displayed: {len(houses_gdf[(houses_gdf['PREZZO'] >= price_range[0]) & (houses_gdf['PREZZO'] <= price_range[1])])}")
    st.write(f"Total number of houses: {len(houses_gdf)}")

if __name__ == "__main__":
    main()