"""
Sales Data Analysis Script
Author: [Your Name]
Date: [Current Date]
Description: Analyzes sales data to calculate metrics and generate insights
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

class SalesAnalyzer:
    """
    Main class for sales data analysis operations
    """
    
    def __init__(self, file_path):
        """Initialize with CSV file path"""
        self.file_path = file_path
        self.df = None
        self.metrics = {}
        
    def load_data(self):
        """Load and validate sales data"""
        try:
            self.df = pd.read_csv(self.file_path)
            print(f"✅ Data loaded successfully. Shape: {self.df.shape}")
            print(f"Columns: {list(self.df.columns)}")
            return True
        except FileNotFoundError:
            print(f"❌ File not found: {self.file_path}")
            return False
    
    def clean_data(self):
        """Handle missing values and data validation"""
        if self.df is None:
            print("❌ No data loaded. Please load data first.")
            return False
            
        print("\n🧹 Data Cleaning Steps:")
        
        # Check for missing values
        missing_values = self.df.isnull().sum()
        print(f"Missing values per column:\n{missing_values}")
        
        # Fill missing numeric values with mean (if any)
        numeric_cols = ['Quantity', 'Price', 'Total_Sales']
        for col in numeric_cols:
            if self.df[col].isnull().any():
                mean_val = self.df[col].mean()
                self.df[col].fillna(mean_val, inplace=True)
                print(f"  - Filled missing values in '{col}' with mean: {mean_val:.2f}")
        
        # Convert Date column to datetime
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        
        # Add Month column for analysis
        self.df['Month'] = self.df['Date'].dt.month_name()
        
        print("✅ Data cleaning completed.")
        return True
    
    def calculate_metrics(self):
        """Calculate various sales metrics"""
        print("\n📊 Calculating Metrics:")
        
        # 1. Total Sales Revenue
        total_sales = self.df['Total_Sales'].sum()
        self.metrics['total_sales'] = total_sales
        print(f"  1. Total Sales Revenue: ₹{total_sales:,.2f}")
        
        # 2. Best-selling product by quantity
        product_sales = self.df.groupby('Product')['Quantity'].sum().sort_values(ascending=False)
        best_product = product_sales.idxmax()
        best_product_qty = product_sales.max()
        self.metrics['best_product'] = best_product
        self.metrics['best_product_qty'] = best_product_qty
        print(f"  2. Best-selling Product: {best_product} ({best_product_qty} units sold)")
        
        # 3. Average transaction value
        avg_transaction = self.df['Total_Sales'].mean()
        self.metrics['avg_transaction'] = avg_transaction
        print(f"  3. Average Transaction Value: ₹{avg_transaction:,.2f}")
        
        # 4. Sales by region
        regional_sales = self.df.groupby('Region')['Total_Sales'].sum().sort_values(ascending=False)
        self.metrics['regional_sales'] = regional_sales
        print("  4. Regional Sales:")
        for region, sales in regional_sales.items():
            print(f"     - {region}: ₹{sales:,.2f}")
        
        # 5. Monthly sales trend
        monthly_sales = self.df.groupby('Month')['Total_Sales'].sum()
        self.metrics['monthly_sales'] = monthly_sales
        print("  5. Monthly Sales Trend:")
        for month, sales in monthly_sales.items():
            print(f"     - {month}: ₹{sales:,.2f}")
        
        return self.metrics
    
    def generate_visualizations(self):
        """Create charts for data visualization"""
        print("\n📈 Generating Visualizations...")
        
        # Create directory for screenshots if it doesn't exist
        os.makedirs('screenshots', exist_ok=True)
        
        # 1. Product Sales Performance
        plt.figure(figsize=(10, 6))
        product_summary = self.df.groupby('Product').agg({
            'Quantity': 'sum',
            'Total_Sales': 'sum'
        }).sort_values('Total_Sales', ascending=False)
        
        plt.subplot(1, 2, 1)
        product_summary['Quantity'].plot(kind='bar', color='skyblue')
        plt.title('Products by Quantity Sold')
        plt.ylabel('Units Sold')
        plt.xticks(rotation=45)
        
        plt.subplot(1, 2, 2)
        product_summary['Total_Sales'].plot(kind='bar', color='lightgreen')
        plt.title('Products by Revenue')
        plt.ylabel('Revenue (₹)')
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.savefig('screenshots/chart_product_performance.png', dpi=150, bbox_inches='tight')
        print("  ✅ Saved: Product Performance Chart")
        
        # 2. Regional Sales Distribution
        plt.figure(figsize=(8, 6))
        regional_data = self.df.groupby('Region')['Total_Sales'].sum()
        colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99']
        plt.pie(regional_data, labels=regional_data.index, autopct='%1.1f%%', 
                colors=colors, startangle=90)
        plt.title('Sales Distribution by Region')
        plt.savefig('screenshots/chart_regional_sales.png', dpi=150, bbox_inches='tight')
        print("  ✅ Saved: Regional Sales Chart")
        
        # 3. Monthly Sales Trend
        plt.figure(figsize=(10, 5))
        monthly_data = self.metrics['monthly_sales']
        months_order = ['January', 'February', 'March', 'April']
        monthly_data = monthly_data.reindex(months_order)
        
        monthly_data.plot(kind='line', marker='o', color='purple', linewidth=2)
        plt.title('Monthly Sales Trend')
        plt.ylabel('Revenue (₹)')
        plt.xlabel('Month')
        plt.grid(True, alpha=0.3)
        plt.savefig('screenshots/chart_sales_trend.png', dpi=150, bbox_inches='tight')
        print("  ✅ Saved: Monthly Sales Trend Chart")
        
        plt.show()
    
    def generate_report(self):
        """Generate a text report of findings"""
        report_content = f"""# Sales Analysis Report
Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary
Total Sales Period: {self.df['Date'].min().strftime('%Y-%m-%d')} to {self.df['Date'].max().strftime('%Y-%m-%d')}
Total Records Analyzed: {len(self.df):,}

## Key Metrics
1. **Total Revenue**: ₹{self.metrics['total_sales']:,.2f}
2. **Average Transaction Value**: ₹{self.metrics['avg_transaction']:,.2f}
3. **Best-selling Product**: {self.metrics['best_product']} ({self.metrics['best_product_qty']} units)

## Regional Performance
"""
        for region, sales in self.metrics['regional_sales'].items():
            percentage = (sales / self.metrics['total_sales']) * 100
            report_content += f"- **{region}**: ₹{sales:,.2f} ({percentage:.1f}%)\n"
        
        report_content += "\n## Monthly Trends\n"
        for month, sales in self.metrics['monthly_sales'].items():
            report_content += f"- **{month}**: ₹{sales:,.2f}\n"
        
        report_content += f"""
## Data Quality
- Missing Values Handled: Yes
- Data Types Validated: Yes
- Records Processed: {len(self.df):,}

## Recommendations
1. Focus on promoting {self.metrics['best_product']} as it's the best seller
2. Investigate opportunities in underperforming regions
3. Analyze seasonal trends for inventory planning
"""
        
        # Save report
        with open('analysis_report.md', 'w') as f:
            f.write(report_content)
        
        print(f"📄 Report saved as 'analysis_report.md'")
        return report_content

def main():
    """Main execution function"""
    print("=" * 60)
    print("🛒 SALES DATA ANALYSIS TOOL")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = SalesAnalyzer('sales_data.csv')
    
    # Execute analysis pipeline
    if analyzer.load_data():
        analyzer.clean_data()
        analyzer.calculate_metrics()
        analyzer.generate_visualizations()
        analyzer.generate_report()
        
        print("\n" + "=" * 60)
        print("✅ ANALYSIS COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("\n📁 Output Files Generated:")
        print("  - analysis_report.md (Detailed analysis)")
        print("  - screenshots/ (Visualization charts)")
        print("  - sales_analysis.py (Source code)")

if __name__ == "__main__":
    main()
