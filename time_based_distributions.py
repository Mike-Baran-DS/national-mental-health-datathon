import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys

# Set style for better visualization
plt.style.use('ggplot')
sns.set_palette("viridis")

# Read CSV data with debugging
file_path = 'processed_call_reports.csv'  # Adjust if your file has a different name

# Try reading with more basic settings first to diagnose the issue
try:
    print("Attempting to read CSV file with basic settings...")
    # Try reading with a specific separator
    df = pd.read_csv(file_path, sep=',', engine='python')
    print(f"Successfully read CSV using basic settings with {len(df)} rows.")
    print(f"Column count: {len(df.columns)}")
    print(f"First few column names: {list(df.columns)[:5]}")
    
    # Display first few rows to verify content
    print("\nFirst 2 rows of data:")
    print(df.head(2).to_string())
    
except Exception as e:
    print(f"Error reading CSV with basic settings: {e}")
    
    # Try an alternative approach with more flexibility
    try:
        print("\nAttempting alternative CSV reading approach...")
        # Using error handling and low memory mode
        df = pd.read_csv(file_path, engine='python', on_bad_lines='skip', low_memory=False)
        print(f"Successfully read CSV using alternative approach with {len(df)} rows.")
    except Exception as e:
        print(f"Error with alternative approach: {e}")
        print("Trying one more method with extreme flexibility...")
        
        # Final attempt with maximum flexibility
        try:
            df = pd.read_csv(file_path, engine='python', on_bad_lines='skip', 
                             delimiter=None, header='infer', skiprows=0)
            print(f"Successfully read CSV with final attempt. Found {len(df)} rows.")
        except Exception as e:
            print(f"All CSV reading attempts failed: {e}")
            sys.exit(1)

# Print DataFrame info to verify what was loaded
print("\nDataFrame Summary:")
print(f"Shape: {df.shape}")
print("\nColumns:")
for col in df.columns:
    print(f"- {col}")

# Check if the expected time columns exist
required_columns = ['Year', 'Month', 'MonthName', 'Day', 'Hour', 'DayOfWeek']
available_columns = [col for col in required_columns if col in df.columns]
missing_columns = [col for col in required_columns if col not in df.columns]

print(f"\nAvailable required columns: {available_columns}")
print(f"Missing required columns: {missing_columns}")

# If no required columns are found, try to identify potential matches
if not available_columns:
    print("\nNone of the required columns found. Looking for potential matches...")
    for col in df.columns:
        for req in required_columns:
            if req.lower() in col.lower():
                print(f"Potential match: '{col}' might correspond to '{req}'")

# Create synthetic data for testing if needed
if not available_columns:
    print("\nCreating synthetic data for testing visualization...")
    # Create a synthetic dataframe with the required columns
    synthetic_df = pd.DataFrame({
        'Year': [2020, 2021, 2022, 2023],
        'Month': [1, 2, 3, 4],
        'MonthName': ['January', 'February', 'March', 'April'],
        'Day': [1, 15, 20, 25],
        'Hour': [9, 12, 15, 18],
        'DayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday']
    })
    
    # Use a few rows of synthetic data to test visualization
    df = synthetic_df
    print("Using synthetic data for visualization test.")
else:
    print("\nUsing actual data for visualization.")

# Creating figure with subplots for each time dimension
print("\nGenerating visualization...")
fig = plt.figure(figsize=(20, 15))
subplot_position = 1

# 1. Year Distribution (if available)
if 'Year' in df.columns:
    ax1 = fig.add_subplot(3, 2, subplot_position)
    subplot_position += 1
    year_counts = df['Year'].value_counts().sort_index()
    print(f"Year counts: {year_counts}")
    sns.barplot(x=year_counts.index, y=year_counts.values, ax=ax1)
    ax1.set_title('Call Distribution by Year', fontsize=16)
    ax1.set_xlabel('Year', fontsize=12)
    ax1.set_ylabel('Number of Calls', fontsize=12)

# 2. Month Distribution (Numeric) (if available)
#if 'Month' in df.columns:
 #   ax2 = fig.add_subplot(3, 2, subplot_position)
  #  subplot_position += 1
   # month_counts = df['Month'].value_counts().sort_index()
    #print(f"Month counts: {month_counts}")
    #sns.barplot(x=month_counts.index, y=month_counts.values, ax=ax2)
    #ax2.set_title('Call Distribution by Month Number', fontsize=16)
    #ax2.set_xlabel('Month Number', fontsize=12)
    #ax2.set_ylabel('Number of Calls', fontsize=12)

# 3. Month Distribution (Name) (if available)
if 'MonthName' in df.columns:
    ax3 = fig.add_subplot(3, 2, subplot_position)
    subplot_position += 1
    # Create a mapping of month names to ensure they're in correct order
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                  'July', 'August', 'September', 'October', 'November', 'December']
    month_name_counts = df['MonthName'].value_counts()
    print(f"Month name counts: {month_name_counts}")
    # Reindex to ensure all months are included in correct order
    month_name_counts = month_name_counts.reindex(month_order, fill_value=0)
    sns.barplot(x=month_name_counts.index, y=month_name_counts.values, ax=ax3)
    ax3.set_title('Call Distribution by Month Name', fontsize=16)
    ax3.set_xlabel('Month Name', fontsize=12)
    ax3.set_ylabel('Number of Calls', fontsize=12)
    ax3.tick_params(axis='x', rotation=45)

# 4. Day Distribution (if available)
if 'Day' in df.columns:
    ax4 = fig.add_subplot(3, 2, subplot_position)
    subplot_position += 1
    day_counts = df['Day'].value_counts().sort_index()
    print(f"Day counts: {day_counts}")
    sns.barplot(x=day_counts.index, y=day_counts.values, ax=ax4)
    ax4.set_title('Call Distribution by Day of Month', fontsize=16)
    ax4.set_xlabel('Day of Month', fontsize=12)
    ax4.set_ylabel('Number of Calls', fontsize=12)

# 5. Hour Distribution (if available)
if 'Hour' in df.columns:
    ax5 = fig.add_subplot(3, 2, subplot_position)
    subplot_position += 1
    hour_counts = df['Hour'].value_counts().sort_index()
    print(f"Hour counts: {hour_counts}")
    sns.barplot(x=hour_counts.index, y=hour_counts.values, ax=ax5)
    ax5.set_title('Call Distribution by Hour of Day', fontsize=16)
    ax5.set_xlabel('Hour of Day', fontsize=12)
    ax5.set_ylabel('Number of Calls', fontsize=12)

# 6. Day of Week Distribution (if available)
if 'DayOfWeek' in df.columns:
    ax6 = fig.add_subplot(3, 2, subplot_position)
    subplot_position += 1
    # Create a mapping of days to ensure they're in correct order
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_week_counts = df['DayOfWeek'].value_counts()
    print(f"Day of week counts: {day_week_counts}")
    # Reindex to ensure all days are included in correct order
    day_week_counts = day_week_counts.reindex(day_order, fill_value=0)
    sns.barplot(x=day_week_counts.index, y=day_week_counts.values, ax=ax6)
    ax6.set_title('Call Distribution by Day of Week', fontsize=16)
    ax6.set_xlabel('Day of Week', fontsize=12)
    ax6.set_ylabel('Number of Calls', fontsize=12)
    ax6.tick_params(axis='x', rotation=45)

# If no subplots were added, add a text box with information
if subplot_position == 1:
    ax = fig.add_subplot(1, 1, 1)
    ax.text(0.5, 0.5, "No time-related columns were found in the data.\n"
            "Please check your CSV file format and column names.",
            horizontalalignment='center', verticalalignment='center',
            fontsize=16)
    ax.axis('off')

# Adjust layout
plt.tight_layout()

# Save the figure with a timestamp to avoid overwriting
import datetime
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
output_filename = f'call_time_distributions_{timestamp}.png'
plt.savefig(output_filename, dpi=300)
print(f"\nCharts generated and saved as '{output_filename}'")

# Force the figure to have content
plt.figtext(0.02, 0.02, f"Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
           fontsize=8, color='gray')

# Save again after adding the timestamp text
plt.savefig(output_filename, dpi=300)
print(f"Visualization saved with timestamp.")

# Show the plot
plt.show()