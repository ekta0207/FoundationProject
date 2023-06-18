#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


# In[9]:


# Load the data
data = pd.read_excel("C:/Users/EKTA PUNDIR/Downloads/Preferrence_Products.xlsx")

# Add a cluster description column
cluster_descriptions = {
     "Hot Picks": "Hot Picks",
     "Well-liked Items": "Well-liked Items",
     "Low-Rated Selections": "Low-Rated Selections"
}
data["Cluster Description"] = data["Category"].map(cluster_descriptions)

# Radio button for cluster selection
selected_cluster = st.sidebar.radio("Select Cluster", options=list(cluster_descriptions.keys()), index=0)


# Filter the data by selected cluster
filtered_data = data[data["Category"] == selected_cluster]

# Check if any items match the selected cluster
if filtered_data.empty:
    st.write("No items found for the selected cluster.")
else:
    # Display top 10 highest selling items
    top_selling_items = filtered_data.nlargest(10, "Number of Reviews")
    st.subheader("Top 10 Highest Selling Items:")
    st.dataframe(top_selling_items)

    # Display details of top selling items
    if not top_selling_items.empty:
        selected_item = st.selectbox("Select an item to view details:", options=top_selling_items["Brand"])
        selected_item_data = top_selling_items[top_selling_items["Brand"] == selected_item]
        st.subheader("Details of Selected Item:")
        st.write(selected_item_data)

    # Display top 10 highest rated items
    top_rated_items = filtered_data.nlargest(10, "Rating")
    st.subheader("Top 10 Highest Rated Items:")
    st.dataframe(top_rated_items)

    # Display scatter plot of volume vs price, colored by brand
    fig_scatter = px.scatter(filtered_data, x="Number of Reviews", y="Market Price (INR)", color="Brand",
                             title="Volume vs Price (Colored by Brand)")
    st.plotly_chart(fig_scatter)
    
    # Trend graph: Amazon volumes per product
    product_volumes = filtered_data.groupby("Brand")["Number of Reviews"].sum()
    fig_volume_trend = px.line(product_volumes, title="Flipkart Volumes per Product")
    st.plotly_chart(fig_volume_trend)

    # Graph: Ratings per product
    fig_ratings = px.box(filtered_data, x="Brand", y="Rating", title="Ratings per Product")
    st.plotly_chart(fig_ratings)

    # Visualization: Sentiment per Product
    fig_sentiment = px.scatter(filtered_data, x="Brand", y="Sentiment Score",
                               title="Sentiment per Product", labels={"Brand": "Brand", "Sentiment Score": "Sentiment Score"})

    st.plotly_chart(fig_sentiment)


    # Search box for keyword filtering
    search_keyword = st.text_input("Search for a keyword:")
    filtered_keyword_data = data[data.apply(lambda row: search_keyword.lower() in row["Product Name"].lower(), axis=1)]
    st.subheader("Filtered Data:")
    st.dataframe(filtered_keyword_data)
    
    # Select Brands manually
    selected_brands = st.sidebar.multiselect("Select Brands", options=data["Brand"].unique())

    # Filter data by selected brands
    filtered_data = data[data["Brand"].isin(selected_brands)]

    # Scatter plot: Volume vs Price, colored by Cluster
    fig_scatter = px.scatter(filtered_data, x="Number of Reviews", y="Current Price (INR)", color="Category", hover_data=["Product Type"],
                         title="Volume vs Price (Colored by Cluster)")
    st.plotly_chart(fig_scatter)
    
    # Convert "Market Price (INR)" column to numeric type
    data["Market Price (INR)"] = pd.to_numeric(data["Market Price (INR)"], errors="coerce")
    
    # Filter by Price slider
    price_min = st.sidebar.slider("Minimum Price", min_value=data["Market Price (INR)"].min(), max_value=data["Market Price (INR)"].max(),
                                  value=data["Market Price (INR)"].min())
    price_max = st.sidebar.slider("Maximum Price", min_value=data["Market Price (INR)"].min(), max_value=data["Market Price (INR)"].max(),
                                  value=data["Market Price (INR)"].max())
    filtered_data = filtered_data[(filtered_data["Market Price (INR)"] >= price_min) & (filtered_data["Market Price (INR)"] <= price_max)]

    # Filter by Rating slider
    rating_min = st.sidebar.slider("Minimum Rating", min_value=data["Rating"].min(), max_value=data["Rating"].max(),
                                   value=data["Rating"].min())
    rating_max = st.sidebar.slider("Maximum Rating", min_value=data["Rating"].min(), max_value=data["Rating"].max(),
                                   value=data["Rating"].max())
    filtered_data = filtered_data[(filtered_data["Rating"] >= rating_min) & (filtered_data["Rating"] <= rating_max)]

    # Density volume plot
    fig_density = px.density_heatmap(filtered_data, x="Current Price (INR)", y="Rating", marginal_x="histogram", marginal_y="histogram",
                                     title="Density Volume of Items")
    st.plotly_chart(fig_density)


