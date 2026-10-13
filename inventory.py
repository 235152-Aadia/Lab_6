
import pandas as pd
import matplotlib.pyplot as plt

# Create product inventory dataset
data = {
    "Product": ["Cola", "Chips", "Milk", "Biscuits", "Juice",
                "Bread", "Water", "Chocolate", "Yogurt", "Tea"],
    "Category": ["beverages ", "SNACKS", " Dairy", "Snacks",
                 "beverages", "DAIRY ", "Beverages", " snacks ",
                 "Dairy", "BEVERAGES"],
    "Price": ["Rs. 1,250", "Rs. 90", "Rs. 450", "Rs. 120",
              "Rs. 1,800", "Rs. 150", "Rs. 50", "Rs. 200",
              "Rs. 180", "Rs. 600"],
    "Stock": [40, 120, 60, 100, 30, 80, 200, 90, 50, 45]
}

df = pd.DataFrame(data)

# Clean category names
df["Category"] = df["Category"].str.strip().str.title()

# Remove currency text and commas, then convert to numbers
df["Price"] = (
    df["Price"]
    .str.replace("Rs. ", "", regex=False)
    .str.replace(",", "", regex=False)
    .astype(float)
)

# Label encoding
df["Category_Code"] = df["Category"].astype("category").cat.codes

# Print cleaned dataset
print("Cleaned Inventory Data:")
print(df)

# Calculate average price by category
avg_price = df.groupby("Category")["Price"].mean()

# Calculate total stock by category
stock_by_category = df.groupby("Category")["Stock"].sum()

# Create two plots side by side
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].bar(avg_price.index, avg_price.values)
axes[0].set_title("Average Price by Category")
axes[0].set_xlabel("Category")
axes[0].set_ylabel("Average Price (Rs.)")
axes[0].tick_params(axis="x", rotation=30)

axes[1].pie(
    stock_by_category.values,
    labels=stock_by_category.index,
    autopct="%1.1f%%",
    startangle=90
)
axes[1].set_title("Share of Total Stock")

plt.tight_layout()
plt.savefig("inventory_plots.png")
plt.show()

print("Saved inventory_plots.png")
