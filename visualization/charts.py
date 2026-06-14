import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class ProductVisualizer:

    def __init__(self, file_path):

        self.df = pd.read_csv(file_path)

        print("\nDataset Loaded Successfully!")

        print(self.df.head())

    def clean_price(self):

        self.df["Price"] = (
            self.df["Price"]
            .astype(str)
            .str.extract(r'(\d[\d,]*)')[0]
            .str.replace(",", "", regex=False)
        )

        self.df["Price"] = pd.to_numeric(
            self.df["Price"],
            errors="coerce"
        )

        self.df.dropna(
            subset=["Price"],
            inplace=True
        )

        print("\nPrice Cleaning Completed!")

    # --------------------------------------
    # NUMPY ANALYSIS
    # --------------------------------------

    def numpy_analysis(self):

        prices = np.array(self.df["Price"])

        print("\nNumPy Statistical Analysis")

        print("Mean Price:", np.mean(prices))

        print("Median Price:", np.median(prices))

        print("Maximum Price:", np.max(prices))

        print("Minimum Price:", np.min(prices))

        print("Standard Deviation:", np.std(prices))

    # --------------------------------------
    # BAR PLOT
    # --------------------------------------

    def top_expensive_products(self):

        top_products = self.df.sort_values(
            by="Price",
            ascending=False
        ).head(10)

        plt.figure(figsize=(14, 6))

        sns.barplot(
            data=top_products,
            x="Price",
            y="Product Name"
        )

        plt.title("Top 10 Expensive Products")

        plt.tight_layout()

        plt.show()

    # --------------------------------------
    # HISTOGRAM
    # --------------------------------------

    def price_distribution(self):

        plt.figure(figsize=(10, 5))

        sns.histplot(
            self.df["Price"],
            bins=20,
            kde=True
        )

        plt.title("Price Distribution")

        plt.tight_layout()

        plt.show()

    # --------------------------------------
    # SCATTER PLOT
    # --------------------------------------

    def scatter_plot(self):

        self.df["Rating"] = pd.to_numeric(
            self.df["Rating"],
            errors="coerce"
        )

        ratings_df = self.df.dropna(
            subset=["Rating"]
        )

        if ratings_df.empty:

            print("No Ratings Available")

            return

        plt.figure(figsize=(8, 5))

        sns.scatterplot(
            x="Rating",
            y="Price",
            data=ratings_df
        )

        plt.title("Rating vs Price")

        plt.show()

    # --------------------------------------
    # BOX PLOT
    # --------------------------------------

    def box_plot(self):

        plt.figure(figsize=(8, 5))

        sns.boxplot(
            x=self.df["Price"]
        )

        plt.title("Boxplot for Price")

        plt.show()

    # --------------------------------------
    # HEATMAP
    # --------------------------------------

    def heatmap(self):

        numeric_df = self.df.select_dtypes(
            include=np.number
        )

        if numeric_df.empty:

            print("No Numeric Data")

            return

        plt.figure(figsize=(8, 5))

        sns.heatmap(
            numeric_df.corr(),
            annot=True,
            cmap="coolwarm"
        )

        plt.title("Correlation Heatmap")

        plt.show()

    # --------------------------------------
    # COUNT PLOT
    # --------------------------------------

    def count_plot(self):

        if "Brand" not in self.df.columns:

            print("Brand column not available")

            return

        plt.figure(figsize=(10, 5))

        sns.countplot(
            y="Brand",
            data=self.df
        )

        plt.title("Brand Count")

        plt.show()

    # --------------------------------------
    # PIE CHART
    # --------------------------------------

    def pie_chart(self):

        if "Brand" not in self.df.columns:

            print("Brand column not available")

            return

        self.df["Brand"].value_counts().head(5).plot.pie(
            autopct="%1.1f%%"
        )

        plt.title("Top Brands")

        plt.ylabel("")

        plt.show()

    # --------------------------------------
    # VIOLIN PLOT
    # --------------------------------------

    def violin_plot(self):

        plt.figure(figsize=(8, 5))

        sns.violinplot(
            x=self.df["Price"]
        )

        plt.title("Violin Plot of Prices")

        plt.show()

    # --------------------------------------
    # KDE PLOT
    # --------------------------------------

    def kde_plot(self):

        plt.figure(figsize=(8, 5))

        sns.kdeplot(
            self.df["Price"],
            fill=True
        )

        plt.title("KDE Plot of Prices")

        plt.show()

    # --------------------------------------
    # RATINGS ANALYSIS
    # --------------------------------------

    def ratings_analysis(self):

        self.df["Rating"] = pd.to_numeric(
            self.df["Rating"],
            errors="coerce"
        )

        ratings_df = self.df.dropna(
            subset=["Rating"]
        )

        if ratings_df.empty:

            print("\nNo valid ratings available.")

            return

        plt.figure(figsize=(8, 5))

        sns.boxplot(
            x=ratings_df["Rating"]
        )

        plt.title("Ratings Analysis")

        plt.show()