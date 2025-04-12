import Header from "../components/Header";
import QueryList from "../components/QueryList";

const mysqlQueries = [
  {
    text: `What are the top 10 product category and sales channel combinations by monthly sales revenue?`,
    category: "Customer & Market Insights",
    queryUrl:
      "http://0.0.0.0:5000/analytics?DB=mysql&query=SELECT%20%0A%20%20%20%20d.year%2C%0A%20%20%20%20d.month%2C%0A%20%20%20%20p.Category%2C%0A%20%20%20%20f.Sales_Channel_%20AS%20sales_channel%2C%0A%20%20%20%20SUM%28fs.amount%29%20AS%20monthly_sales%0AFROM%20FactSales%20fs%0AJOIN%20DimDate%20d%20ON%20fs.date_id%20%3D%20d.date_id%0AJOIN%20DimProduct%20p%20ON%20fs.product_id%20%3D%20p.product_id%0AJOIN%20DimFulfillment%20f%20ON%20fs.fulfillment_id%20%3D%20f.fulfillment_id%0AGROUP%20BY%20d.year%2C%20d.month%2C%20p.Category%2C%20f.Sales_Channel_%0AORDER%20BY%20monthly_sales%20DESC%0ALIMIT%2010%3B",
  },
  {
    text: "Who are the top 10 most loyal or active customers based on the number of orders?",
    category: "Customer & Market Insights",
    queryUrl:
      "http://0.0.0.0:5000/analytics?DB=mysql&query=SELECT%20%0A%20%20%20%20fs.customer_id%2C%0A%20%20%20%20COUNT%28fs.order_id%29%20AS%20total_orders%2C%0A%20%20%20%20Round%28SUM%28fs.amount%29%2C%203%29%20AS%20total_spent%0AFROM%20FactSales%20fs%0AGROUP%20BY%20fs.customer_id%0AORDER%20BY%20total_orders%20DESC%0ALIMIT%2010",
  },

  {
    text: "What is the distribution of cancelled and returned orders by status type?",
    category: "Operational Efficiency",
    queryUrl:
      "http://0.0.0.0:5000/analytics?DB=mysql&query=SELECT%20%0A%20%20%20%20os.status_name%20AS%20order_status%2C%0A%20%20%20%20COUNT%28fs.order_id%29%20AS%20total_orders%0AFROM%20FactSales%20fs%0AJOIN%20DimOrderStatus%20os%20ON%20fs.status_id%20%3D%20os.status_id%0AWHERE%20os.status_name%20IN%20%28%0A%20%20%20%20%27Cancelled%27%2C%0A%20%20%20%20%27Shipped%20-%20Returned%20to%20Seller%27%2C%0A%20%20%20%20%27Shipped%20-%20Rejected%20by%20Buyer%27%2C%0A%20%20%20%20%27Shipped%20-%20Lost%20in%20Transit%27%2C%0A%20%20%20%20%27Shipped%20-%20Returning%20to%20Seller%27%2C%0A%20%20%20%20%27Shipped%20-%20Damaged%27%0A%29%0AGROUP%20BY%20os.status_name%0AORDER%20BY%20total_orders%20DESC%3B%0A",
  },
  {
    text: "What is the total gross sales revenue generated in April 2022 across all channels and products?",
    category: "Sales Performance",
    queryUrl:
      "http://0.0.0.0:5000/analytics?DB=mysql&query=SELECT%20%0A%09p.category%2C%20%0A%20%20%20%20f.Sales_Channel_%2C%0A%20%20%20%20SUM%28fs.amount%29%20AS%20total_sales%0AFROM%20FactSales%20fs%0AJOIN%20DimDate%20d%20ON%20fs.date_id%20%3D%20d.date_id%0AJOIN%20DimProduct%20p%20ON%20fs.product_id%20%3D%20p.product_id%20%0AJOIN%20DimFulfillment%20f%20ON%20fs.fulfillment_id%20%3D%20f.fulfillment_id%0AWHERE%20d.year%20%3D%202022%20AND%20d.month%20%3D%204%0AGROUP%20BY%20p.category%2C%20f.Sales_Channel_%3B",
  },

  {
    text: "Which top 10 SKUs generated the highest gross sales revenue in April 2022, considering their category, size, style, and sales channel?",
    category: "Sales Performance",
    queryUrl:
      "http://0.0.0.0:5000/analytics?DB=mysql&query=SELECT%20%0A%20%20%20%20p.SKU%2C%0A%20%20%20%20p.Category%2C%0A%20%20%20%20p.Size%2C%0A%20%20%20%20p.Style%2C%0A%20%20%20%20f.Sales_Channel_%2C%0A%20%20%20%20SUM%28fs.amount%29%20AS%20total_gross_sales%0AFROM%20FactSales%20fs%0AJOIN%20DimProduct%20p%20ON%20fs.product_id%20%3D%20p.product_id%0AJOIN%20DimFulfillment%20f%20ON%20fs.fulfillment_id%20%3D%20f.fulfillment_id%0AJOIN%20DimDate%20d%20ON%20fs.date_id%20%3D%20d.date_id%0AWHERE%20d.year%20%3D%202022%20AND%20d.month%20%3D%204%0AGROUP%20BY%20p.SKU%2C%20p.Category%2C%20p.Size%2C%20p.Style%2C%20f.Sales_Channel_%0AORDER%20BY%20total_gross_sales%20DESC%0ALIMIT%2010%3B%0ASELECT%20%2A%20FROM%20%60DimProduct%60%20WHERE%2011",
  },

  {
    text: "What are the total sales by order status?",
    category: "Sales Performance",
    queryUrl:
      "http://0.0.0.0:5000/analytics?DB=mysql&query=SELECT%20%0A%20%20%20%20os.status_name%20AS%20order_status%2C%0A%20%20%20%20COUNT%28fs.order_id%29%20AS%20total_orders%2C%0A%20%20%20%20SUM%28fs.amount%29%20AS%20total_sales%0AFROM%20FactSales%20fs%0AJOIN%20DimOrderStatus%20os%20ON%20fs.status_id%20%3D%20os.status_id%0AGROUP%20BY%20os.status_name%0AORDER%20BY%20total_sales%20DESC%3B",
  },

  {
    text: "What is the total number of orders and gross sales revenue for each order status?",
    category: "Sales Performance",
    queryUrl:
      "http://0.0.0.0:5000/analytics?DB=mysql&query=SELECT%20%0A%20%20%20%20d.year%2C%0A%20%20%20%20d.month%2C%0A%20%20%20%20SUM%28fs.amount%29%20AS%20total_monthly_sales%0AFROM%20FactSales%20fs%0AJOIN%20DimDate%20d%20ON%20fs.date_id%20%3D%20d.date_id%0AGROUP%20BY%20d.year%2C%20d.month%0AORDER%20BY%20d.year%2C%20d.month%3B",
  },

  {
    text: "Which top 5 product sizes are the most frequently ordered among items that have been shipped?",
    category: "Inventory & Product Analysis",
    queryUrl:
      "http://0.0.0.0:5000/analytics?DB=mysql&query=SELECT%20%0A%20%20%20%20p.Size%2C%0A%20%20%20%20COUNT%28fs.order_id%29%20AS%20total_shipped_orders%0AFROM%20FactSales%20fs%0AJOIN%20DimProduct%20p%20ON%20fs.product_id%20%3D%20p.product_id%0AJOIN%20DimOrderStatus%20os%20ON%20fs.status_id%20%3D%20os.status_id%0AWHERE%20os.status_name%20LIKE%20%27Shipped%25%27%0AGROUP%20BY%20p.Size%0AORDER%20BY%20total_shipped_orders%20DESC%0ALIMIT%205%3B",
  },

  {
    text: "Which top 10 products generated the highest total gross sales revenue across all time?",
    category: "Inventory & Product Analysis",
    queryUrl:
      "http://0.0.0.0:5000/analytics?DB=mysql&query=SELECT%20%0A%20%20%20%20p.SKU%2C%0A%20%20%20%20p.Category%2C%0A%20%20%20%20p.Size%2C%0A%20%20%20%20p.Style%2C%0A%20%20%20%20SUM%28fs.amount%29%20AS%20total_revenue%0AFROM%20FactSales%20fs%0AJOIN%20DimProduct%20p%20ON%20fs.product_id%20%3D%20p.product_id%0AGROUP%20BY%20p.SKU%2C%20p.Category%2C%20p.Size%2C%20p.Style%0AORDER%20BY%20total_revenue%20DESC%0ALIMIT%2010%3B%0A",
  },
  {
    text: "What is the total sales distribution across product categories, based on gross revenue and order volume?",
    category: "Inventory & Product Analysis",
    queryUrl:
      "http://0.0.0.0:5000/analytics?DB=mysql&query=SELECT%0A%09p.Category%2C%20%0A%20%20%20%20COUNT%28fs.order_id%29%20AS%20total_orders%2C%20%0A%20%20%20%20SUM%28fs.amount%29%20AS%20total_revenue%0AFROM%20FactSales%20fs%20%0AJOIN%20DimProduct%20p%20ON%20fs.product_id%20%3D%20p.product_id%0AGROUP%20BY%20p.Category%0AORDER%20BY%20total_revenue%20DESC",
  },
];

const MySQLPage = () => {
  return (
    <div>
      <Header />
      <h1 className="text-3xl font-bold text-center mt-6">
        Welcome to MySQL Page
      </h1>
      <QueryList queries={mysqlQueries} />
    </div>
  );
};

export default MySQLPage;
