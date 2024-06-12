import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
from tabulate import tabulate
import seaborn as sns

# URL for web scraping
url = "https://www.iplt20.com/auction/2022"

# Fetch the content from the URL
r = requests.get(url)

print("Request Status : ")
print(r.status_code)  # Print the status code to ensure the request was successful

print("\n" + "" * 80 + "\n")

# Parse the HTML content using BeautifulSoup with the lxml parser
soup = BeautifulSoup(r.text, "lxml")

# Find the table with the specified class
table = soup.find("table", class_="ih-td-tab auction-tbl")

# Extract headers
headers = table.find_all("th")
header_names = [header.text.strip() for header in headers]
print(header_names)  # Debugging print to see the headers

# Initialize the DataFrame with the headers
df = pd.DataFrame(columns=header_names)

# Extract data rows and populate the DataFrame
rows = table.find_all("tr")   # Table Row

for row in rows[1:]:  # Skip the header row
    cols = row.find_all("td")  # Table Data
    data = [col.text.strip() for col in cols]

    if len(data) == len(header_names):  # Ensure row has the same number of columns as the header
        df.loc[len(df)] = data
    else:
        print(f"Skipping row due to mismatched columns: {data}")  # Debugging print for problematic rows

# Print the DataFrame with borders using tabulate
print(tabulate(df, headers='keys', tablefmt='grid'))

# Save the DataFrame to a CSV file
df.to_csv("IPL Auction Stats.csv", index=False)

# -----------------------------------------------------------------------
# -----------------------------------------------------------------------

# Convert relevant columns to numeric values for plotting
df['FUNDS REMAINING'] = df['FUNDS REMAINING'].str.replace('₹', '').str.replace(',', '').astype(int)
df['OVERSEAS PLAYERS'] = df['OVERSEAS PLAYERS'].astype(int)
df['TOTAL PLAYERS'] = df['TOTAL PLAYERS'].astype(int)

print("\n" + "" * 80 + "\n")
print("\n" + "" * 80 + "\n")

# 1. Funds Remaining by Team
#cmap = get_cmap("tab10")
colors = [cmap(i) for i in range(len(df))]
plt.figure(figsize=(10, 6))
plt.barh(df['TEAM'], df['FUNDS REMAINING'], color=colors)
plt.xlabel('Funds Remaining (in ₹)')
plt.ylabel('Team')
plt.title('Funds Remaining by Team')
plt.gca().invert_yaxis()  # Invert y-axis to display team with highest funds on top
plt.show()

print("\n" + "" * 80 + "\n")
print("\n" + "" * 80 + "\n")

# 2. Number of Overseas Players
plt.figure(figsize=(10, 6))
plt.barh(df['TEAM'], df['OVERSEAS PLAYERS'], color=colors)
plt.xlabel('Number of Overseas Players')
plt.ylabel('Team')
plt.title('Number of Overseas Players by Team')
plt.gca().invert_yaxis()  # Invert y-axis to display team with highest number of overseas players on top
plt.show()

print("\n" + "" * 80 + "\n")
print("\n" + "" * 80 + "\n")

# 3. Total Players
plt.figure(figsize=(10, 6))
plt.barh(df['TEAM'], df['TOTAL PLAYERS'], color=colors)
plt.xlabel('Total Players')
plt.ylabel('Team')
plt.title('Total Players by Team')
plt.gca().invert_yaxis()  # Invert y-axis to display team with highest number of players on top
plt.show()

print("\n" + "" * 80 + "\n")
print("\n" + "" * 80 + "\n")

# 4. Distribution of Overseas Players (Pie Chart)
plt.figure(figsize=(8, 8))
plt.pie(df['OVERSEAS PLAYERS'], labels=df['TEAM'], autopct='%1.1f%%', startangle=140, colors=colors)
plt.title('Distribution of Overseas Players')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
plt.show()

print("\n" + "" * 80 + "\n")
print("\n" + "" * 80 + "\n")

# 5. Funds Remaining Distribution (Box Plot)
plt.figure(figsize=(8, 6))
plt.boxplot(df['FUNDS REMAINING'])
plt.title('Distribution of Funds Remaining')
plt.ylabel('Funds Remaining (in ₹)')
plt.show()

print("\n" + "" * 80 + "\n")
print("\n" + "" * 80 + "\n")


# 6. Histogram of Funds Remaining
plt.figure(figsize=(10, 6))
plt.hist(df['FUNDS REMAINING'], bins=10, color='skyblue')
plt.title('Histogram of Funds Remaining')
plt.xlabel('Funds Remaining (in ₹)')
plt.ylabel('Number of Teams')
plt.show()

print("\n" + "" * 80 + "\n")
print("\n" + "" * 80 + "\n")

# 7. Scatter Plot of Funds Remaining vs. Total Players
plt.figure(figsize=(10, 6))
plt.scatter(df['TOTAL PLAYERS'], df['FUNDS REMAINING'], color='green')
plt.title('Scatter Plot of Funds Remaining vs. Total Players')
plt.xlabel('Total Players')
plt.ylabel('Funds Remaining (in ₹)')
plt.show()

print("\n" + "" * 80 + "\n")
print("\n" + "" * 80 + "\n")

# 8. Stacked Bar Chart of Local vs. Overseas Players
df['LOCAL PLAYERS'] = df['TOTAL PLAYERS'] - df['OVERSEAS PLAYERS']
df.set_index('TEAM', inplace=True)
df[['LOCAL PLAYERS', 'OVERSEAS PLAYERS']].plot(kind='bar', stacked=True, figsize=(10, 6), color=['#1f77b4', '#ff7f0e'])
plt.xlabel('Team')
plt.ylabel('Number of Players')
plt.title('Local vs. Overseas Players by Team')
plt.show()

print("\n" + "" * 80 + "\n")
print("\n" + "" * 80 + "\n")
