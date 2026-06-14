from scraper.flipkart_scraper import FlipkartScraper
from visualization.charts import ProductVisualizer


def run_project():

    print("\n===================================")
    print(" Flipkart Web Scraping & EDA Project ")
    print("===================================\n")

    # --------------------------------------
    # USER INPUT
    # --------------------------------------

    product = input("Enter Product Name: ")

    try:

        pages = int(input("Enter Number of Pages: "))

    except ValueError:

        print("Invalid page number!")

        return

    # --------------------------------------
    # SCRAPING
    # --------------------------------------

    print("\nStarting Web Scraping...\n")

    scraper = FlipkartScraper(
        product_name=product,
        pages=pages
    )

    scraper.scrape()

    df = scraper.save_data()

    # --------------------------------------
    # CHECK DATA
    # --------------------------------------

    if df is None:

        print("\nNo data scraped!")

        return

    print("\nScraping Completed Successfully!")

    # --------------------------------------
    # VISUALIZATION & EDA
    # --------------------------------------

    print("\nStarting EDA & Visualization...\n")

    visualizer = ProductVisualizer(
        "data/flipkart_products.csv"
    )

    # --------------------------------------
    # DATA CLEANING
    # --------------------------------------

    visualizer.clean_price()

    # --------------------------------------
    # NUMPY / STATISTICS
    # --------------------------------------

    visualizer.numpy_analysis()

    # --------------------------------------
    # UNIVARIATE ANALYSIS
    # --------------------------------------

    print("\nGenerating Histogram...\n")
    visualizer.price_distribution()

    print("\nGenerating Box Plot...\n")
    visualizer.box_plot()

    print("\nGenerating KDE Plot...\n")
    visualizer.kde_plot()

    print("\nGenerating Violin Plot...\n")
    visualizer.violin_plot()

    # --------------------------------------
    # TOP PRODUCTS
    # --------------------------------------

    print("\nGenerating Top Expensive Products Chart...\n")
    visualizer.top_expensive_products()

    # --------------------------------------
    # BIVARIATE ANALYSIS
    # --------------------------------------

    print("\nGenerating Scatter Plot...\n")
    visualizer.scatter_plot()

    print("\nGenerating Heatmap...\n")
    visualizer.heatmap()

    # --------------------------------------
    # CATEGORICAL ANALYSIS
    # --------------------------------------

    print("\nGenerating Count Plot...\n")
    visualizer.count_plot()

    print("\nGenerating Pie Chart...\n")
    visualizer.pie_chart()

    # --------------------------------------
    # RATINGS ANALYSIS
    # --------------------------------------

    print("\nGenerating Ratings Analysis...\n")
    visualizer.ratings_analysis()

    # --------------------------------------
    # COMPLETION MESSAGE
    # --------------------------------------

    print("\n===================================")
    print(" Project Execution Completed ")
    print("===================================\n")


if __name__ == "__main__":

    run_project()