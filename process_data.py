"""
Mental Health Datathon - Date/Time Processing Script
===================================================

This script processes call report data from a CSV file, focusing on extracting
temporal features from a datetime column. It creates a new DataFrame with additional
columns for year, month, day, hour, and day of week to enable time-based analysis.

Usage:
------
1. Ensure Python 3.7+ is installed
2. Set up virtual environment as described in setup instructions
3. Run this script from the project directory
4. Output will be saved as 'processed_call_reports.csv'

Author: [Mike Baran]
Date: April 6, 2025
"""

import os
import pandas as pd
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_processing.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()


def create_datetime_features(input_file, output_file):
    """
    Process call report data by extracting date/time features.

    Parameters:
    -----------
    input_file : str
        Path to the input CSV file containing call report data
    output_file : str
        Path where the processed CSV file will be saved

    Returns:
    --------
    pd.DataFrame
        Processed DataFrame with additional date/time features
    """
    try:
        # Check if input file exists
        if not os.path.exists(input_file):
            logger.error(f"Input file not found: {input_file}")
            return None

        # Read the data
        logger.info(f"Reading data from {input_file}")
        df = pd.read_csv(input_file)

        # Check if the required column exists
        if 'CallDateAndTimeStart' not in df.columns:
            logger.error(
                "Required column 'CallDateAndTimeStart' not found in the dataset")
            return None

        # Display initial data info
        logger.info(f"Initial data shape: {df.shape}")

        # Convert to datetime format
        logger.info("Converting 'CallDateAndTimeStart' to datetime")
        df['CallDateAndTimeStart'] = pd.to_datetime(
            df['CallDateAndTimeStart'],
            errors='coerce'  # Convert invalid values to NaT
        )

        # Log missing values after conversion
        nat_count = df['CallDateAndTimeStart'].isna().sum()
        if nat_count > 0:
            logger.warning(
                f"Found {nat_count} invalid date values that were converted to NaT")

        # Extract date components
        logger.info("Extracting date and time components")
        df['Year'] = df['CallDateAndTimeStart'].dt.year
        df['Month'] = df['CallDateAndTimeStart'].dt.month
        df['MonthName'] = df['CallDateAndTimeStart'].dt.month_name()
        df['Day'] = df['CallDateAndTimeStart'].dt.day
        df['Hour'] = df['CallDateAndTimeStart'].dt.hour
        df['DayOfWeek'] = df['CallDateAndTimeStart'].dt.day_name()

        # Save processed data
        logger.info(f"Saving processed data to {output_file}")
        df.to_csv(output_file, index=False)

        # Return summary statistics
        logger.info("Processing completed successfully")
        return df

    except Exception as e:
        logger.error(f"Error processing data: {str(e)}")
        return None


def main():
    """
    Main function to execute the data processing workflow.
    """
    # Define file paths
    project_folder = "/Users/mikebaran/Desktop/National Mental Health Datathon"
    input_file = os.path.join(project_folder, "Primary_CallReports_v1.2.csv")
    output_file = os.path.join(project_folder, "processed_call_reports.csv")

    # Process the data
    processed_data = create_datetime_features(input_file, output_file)

    if processed_data is not None:
        # Display sample of processed data
        print("\nSample of processed data:")
        cols_to_show = ['CallDateAndTimeStart', 'Year',
                        'Month', 'MonthName', 'Day', 'Hour', 'DayOfWeek']
        print(processed_data[cols_to_show].head())

        # Display summary statistics
        print("\nDistribution by day of week:")
        print(processed_data['DayOfWeek'].value_counts())

        print("\nDistribution by hour:")
        print(processed_data['Hour'].value_counts().sort_index())


if __name__ == "__main__":
    main()
