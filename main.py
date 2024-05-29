import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.iplt20.com/auction/2022"

# Fetch the content from the URL
r = requests.get(url)
print(r.status_code)  # Print the status code to ensure the request was successful

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
rows = table.find_all("tr")
for row in rows[1:]:  # Skip the header row
    cols = row.find_all("td")
    data = [col.text.strip() for col in cols]
    if len(data) == len(header_names):  # Ensure row has the same number of columns as the header
        df.loc[len(df)] = data
    else:
        print(f"Skipping row due to mismatched columns: {data}")  # Debugging print for problematic rows

print(df)
df.to_csv("IPL Auction Stats.csv", index=False);

import matplotlib.pyplot as plt

# 1. Funds Remaining by Team
plt.figure(figsize=(10, 6))
plt.barh(df['TEAM'], df['FUNDS REMAINING'].str.replace('₹', '').str.replace(',', '').astype(int), color='skyblue')
plt.xlabel('Funds Remaining (in ₹)')
plt.ylabel('Team')
plt.title('Funds Remaining by Team')
plt.gca().invert_yaxis()  # Invert y-axis to display team with highest funds on top
plt.show()

# 2. Number of Overseas Players
plt.figure(figsize=(10, 6))
plt.barh(df['TEAM'], df['OVERSEAS PLAYERS'].astype(int), color='lightgreen')
plt.xlabel('Number of Overseas Players')
plt.ylabel('Team')
plt.title('Number of Overseas Players by Team')
plt.gca().invert_yaxis()  # Invert y-axis to display team with highest number of overseas players on top
plt.show()

# 3. Total Players
plt.figure(figsize=(10, 6))
plt.barh(df['TEAM'], df['TOTAL PLAYERS'].astype(int), color='salmon')
plt.xlabel('Total Players')
plt.ylabel('Team')
plt.title('Total Players by Team')
plt.gca().invert_yaxis()  # Invert y-axis to display team with highest number of players on top
plt.show()

# 4. Summary Statistics - Funds Remaining
summary_stats = df['FUNDS REMAINING'].str.replace('₹', '').str.replace(',', '').astype(int).describe()
print("Summary Statistics for Funds Remaining:")
print(summary_stats)
import matplotlib.pyplot as plt

# 1. Funds Remaining by Team
plt.figure(figsize=(10, 6))
plt.barh(df['TEAM'], df['FUNDS REMAINING'].str.replace('₹', '').str.replace(',', '').astype(int), color='skyblue')
plt.xlabel('Funds Remaining (in ₹)')
plt.ylabel('Team')
plt.title('Funds Remaining by Team')
plt.gca().invert_yaxis()  # Invert y-axis to display team with highest funds on top
plt.show()

# 2. Number of Overseas Players
plt.figure(figsize=(10, 6))
plt.barh(df['TEAM'], df['OVERSEAS PLAYERS'].astype(int), color='lightgreen')
plt.xlabel('Number of Overseas Players')
plt.ylabel('Team')
plt.title('Number of Overseas Players by Team')
plt.gca().invert_yaxis()  # Invert y-axis to display team with highest number of overseas players on top
plt.show()

# 3. Total Players
plt.figure(figsize=(10, 6))
plt.barh(df['TEAM'], df['TOTAL PLAYERS'].astype(int), color='salmon')
plt.xlabel('Total Players')
plt.ylabel('Team')
plt.title('Total Players by Team')
plt.gca().invert_yaxis()  # Invert y-axis to display team with highest number of players on top
plt.show()


import matplotlib.pyplot as plt

# 1. Funds Remaining Distribution (Box Plot)
plt.figure(figsize=(8, 6))
plt.boxplot(df['FUNDS REMAINING'].str.replace('₹', '').str.replace(',', '').astype(int))
plt.title('Distribution of Funds Remaining')
plt.ylabel('Funds Remaining (in ₹)')
plt.show()

# 2. Distribution of Overseas Players (Pie Chart)
plt.figure(figsize=(8, 8))
plt.pie(df['OVERSEAS PLAYERS'].astype(int), labels=df['TEAM'], autopct='%1.1f%%', startangle=140)
plt.title('Distribution of Overseas Players')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
plt.show()

# 3. Distribution of Total Players (Pie Chart)
plt.figure(figsize=(8, 8))
plt.pie(df['TOTAL PLAYERS'].astype(int), labels=df['TEAM'], autopct='%1.1f%%', startangle=140)
plt.title('Distribution of Total Players')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
plt.show()



