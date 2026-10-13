
import pandas as pd
import matplotlib.pyplot as plt

# Create 15 days of weather data
data = {
    "Date": [
        "2026-01-01", "2026-01-02", "2026-01-03",
        "2026-01-04", "2026-01-05", "2026-01-06",
        "2026-01-07", "2026-01-08", "2026-01-09",
        "2026-01-10", "2026-01-11", "2026-01-12",
        "2026-01-13", "2026-01-14", "2026-01-15",
        "2026-01-01"
    ],
    "City": [
        " lahore", "LAHORE ", "Islamabad", " karachi",
        "LAHORE", "Islamabad ", "KARACHI", "Lahore",
        "islamabad", "Karachi ", " lahore", "ISLAMABAD",
        "Karachi", "Lahore ", "Islamabad", " lahore"
    ],
    "Temperature": [
        "32C", "30C", "28C", "35C", "31C", "27C",
        "34C", "29C", "26C", "33C", "32C", "25C",
        "36C", "30C", "28C", "32C"
    ],
    "Humidity": [
        45, 50, None, 40, 55, 60, None, 52,
        65, 42, None, 68, 38, 57, 62, 45
    ],
    "Condition": [
        "sunny", "CLOUDY ", "Rainy", " Sunny ",
        "cloudy", "SUNNY", " rainy ", "Sunny",
        "Cloudy", "SUNNY ", "sunny", "cloudy",
        "RAINY", "Sunny", " cloudy ", "sunny"
    ]
}

df = pd.DataFrame(data)

# Clean text columns
for col in ["City", "Condition"]:
    df[col] = df[col].str.strip().str.title()

# Convert temperature from text to numeric
df["Temperature"] = (
    df["Temperature"]
    .str.replace("C", "", regex=False)
    .astype(float)
)

# Convert date strings to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Remove duplicate rows
df = df.drop_duplicates().copy()

print("Rows after dropping duplicates:", len(df))

# Fill missing humidity with the median
humidity_median = df["Humidity"].median()
df["Humidity"] = df["Humidity"].fillna(humidity_median)

print("Missing Humidity filled with median:", humidity_median)

# One-hot encode the Condition column
df_encoded = pd.get_dummies(
    df, columns=["Condition"], dtype=int
)

print("\nEncoded Condition Columns:")
print(df_encoded.filter(like="Condition_").head())

# Calculate correlation
correlation = df["Temperature"].corr(df["Humidity"])
print("\nCorrelation (Temperature, Humidity):",
      round(correlation, 3))

# Count weather conditions
condition_counts = df["Condition"].value_counts()
print("\nCondition counts:")
print(condition_counts)

# Create four plots in a 2 x 2 dashboard
fig, axes = plt.subplots(2, 2, figsize=(12, 9))

# 1. Temperature over time
axes[0, 0].plot(
    df["Date"], df["Temperature"], marker="o"
)
axes[0, 0].set_title("Temperature Over Date")
axes[0, 0].set_xlabel("Date")
axes[0, 0].set_ylabel("Temperature (C)")
axes[0, 0].tick_params(axis="x", rotation=45)

# 2. Temperature versus humidity
axes[0, 1].scatter(
    df["Temperature"], df["Humidity"]
)
axes[0, 1].set_title("Temperature vs Humidity")
axes[0, 1].set_xlabel("Temperature (C)")
axes[0, 1].set_ylabel("Humidity")

# 3. Number of days for each condition
axes[1, 0].pie(
    condition_counts.values,
    labels=condition_counts.index,
    autopct="%1.1f%%",
    startangle=90
)
axes[1, 0].set_title("Weather Conditions")

# 4. Temperature distribution
axes[1, 1].hist(
    df["Temperature"], bins=5, edgecolor="black"
)
axes[1, 1].set_title("Temperature Distribution")
axes[1, 1].set_xlabel("Temperature (C)")
axes[1, 1].set_ylabel("Number of Days")

fig.suptitle("Weather Overview", fontsize=16)
plt.tight_layout()
plt.savefig("weather_dashboard.png")
plt.show()

print("\nSaved weather_dashboard.png")
