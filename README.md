## LA Bike Share Data ETL and Visualization Project

### Overview

This project aims to extract, transform, and load (ETL) data from the LA Bike Share Data website into Google Cloud Storage, perform data processing using Docker and Mage AI, load the processed data into BigQuery, and visualize the insights gained from the data using Tableau.

### Data Architecture

The data architecture of this project involves several components:

1. **Data Extraction**: LA Bike Share data is collected from the official LA Bike Share Data website. This data includes information about bike rides, stations, users, and more.

2. **Storage**: The extracted data is stored in Google Cloud Storage (GCS). GCS provides a scalable and reliable storage solution for large datasets.

3. **ETL Process**: The Extract, Transform, Load (ETL) process is performed using Docker containers and Mage AI. Mage AI automates data integration and transformation tasks, allowing for efficient ETL workflows.

4. **Data Warehousing**: Processed data is loaded into Google BigQuery, a fully managed, serverless data warehouse. BigQuery allows for fast SQL queries and real-time analytics on large datasets.

5. **Visualization**: Tableau is used for data visualization. Tableau provides powerful tools for creating interactive dashboards and visualizations to explore and analyze the data.
