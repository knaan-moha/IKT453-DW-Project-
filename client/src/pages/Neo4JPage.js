import Header from "../components/Header";
import QueryList from "../components/QueryList";

const neo4jQueries = [
  {
    text: "What are the top 10 product category and sales channel combinations by monthly sales revenue?",
    category: "Customer & Market Insights",
    queryUrl: "http://localhost:5000/analytics?DB=neo4j&query=MATCH%20(fs%3Afact_sales)-%5B%3AHAS_DATE%5D-%3E(d%3Adim_date)%2C%0A%20%20%20%20(fs)-%5B%3AHAS_PRODUCT%5D-%3E(p%3Adim_product)%2C%0A%20%20%20%20(fs)-%5B%3AHAS_FULFILLMENT%5D-%3E(f%3Adim_fulfillment)%0ARETURN%0A%20%20%20%20d.year%20AS%20year%2C%0A%20%20%20%20d.month%20AS%20month%2C%0A%20%20%20%20p.Category%20AS%20category%2C%0A%20%20%20%20f.Sales_Channel_%20AS%20sales_channel%2C%0A%20%20%20%20toInteger(SUM(toFloat(fs.amount)))%20AS%20monthly_sales%0AORDER%20BY%20monthly_sales%20DESC%0ALIMIT%2010",
  },
  {
    text: "Who are the top 10 most loyal or active customers based on the number of orders?",
    category: "Customer & Market Insights",
    queryUrl:
      "http://localhost:5000/analytics?DB=neo4j&query=MATCH%20%28f%3Afact_sales%29%0AWITH%20f.customer_id%20AS%20customer_id%2C%20COUNT%28f%29%20AS%20total_orders%2C%20ROUND%28SUM%28toFloat%28f.amount%29%29%2C%203%29%20AS%20total_spent%0ARETURN%20customer_id%2C%20total_orders%2C%20total_spent%0AORDER%20BY%20total_orders%20DESC%0ALIMIT%2010",
  },


  {
    text: "What is the distribution of cancelled and returned orders by status type?",
    category: "Operational Efficiency",
    queryUrl:
      "http://localhost:5000/analytics?DB=neo4j&query=MATCH%20%28f%3Afact_sales%29-%5B%3AHAS_STATUS%5D-%3E%28s%3Adim_status%29%0AWHERE%20s.status_name%20IN%20%5B%0A%20%20%20%20%27Cancelled%27%2C%0A%20%20%20%20%27Shipped%20-%20Returned%20to%20Seller%27%2C%0A%20%20%20%20%27Shipped%20-%20Rejected%20by%20Buyer%27%2C%0A%20%20%20%20%27Shipped%20-%20Lost%20in%20Transit%27%2C%0A%20%20%20%20%27Shipped%20-%20Returning%20to%20Seller%27%2C%0A%20%20%20%20%27Shipped%20-%20Damaged%27%0A%5D%0AWITH%20%0A%20%20%20%20s.status_name%20AS%20order_status%2C%0A%20%20%20%20COUNT%28f.order_id%29%20AS%20total_orders%0ARETURN%20%0A%20%20%20%20order_status%2C%0A%20%20%20%20total_orders%0AORDER%20BY%20total_orders%20DESC",
  },
  {
    text: "What is the total gross sales revenue generated in April 2022 across all channels and products?",
    category: "Sales Performance",
    queryUrl:
      "http://localhost:5000/analytics?DB=neo4j&query=MATCH%20%28fs%3Afact_sales%29-%5B%3AHAS_DATE%5D-%3E%28d%3Adim_date%29%2C%0A%20%20%20%20%20%20%28fs%29-%5B%3AHAS_PRODUCT%5D-%3E%28p%3Adim_product%29%2C%0A%20%20%20%20%20%20%28fs%29-%5B%3AHAS_FULFILLMENT%5D-%3E%28f%3Adim_fulfillment%29%0AWHERE%20d.year%20%3D%20%222022%22%20AND%20d.month%20%3D%20%224%22%0AWITH%20%0A%20%20%20%20p.Category%20AS%20category%2C%0A%20%20%20%20f.Sales_Channel_%20AS%20sales_channel%2C%0A%20%20%20%20SUM%28toFloat%28fs.amount%29%29%20AS%20total_sales%0ARETURN%20%0A%20%20%20%20category%2C%0A%20%20%20%20sales_channel%2C%0A%20%20%20%20total_sales%0AORDER%20BY%20total_sales%20DESC",
  },
  {
    text: "Which top 10 SKUs generated the highest gross sales revenue in April 2022, considering their category, size, style, and sales channel?",
    category: "Sales Performance",
    queryUrl:
      "http://localhost:5000/analytics?DB=neo4j&query=MATCH%20%28fs%3Afact_sales%29-%5B%3AHAS_PRODUCT%5D-%3E%28p%3Adim_product%29%2C%0A%20%20%20%20%20%20%28fs%29-%5B%3AHAS_FULFILLMENT%5D-%3E%28f%3Adim_fulfillment%29%2C%0A%20%20%20%20%20%20%28fs%29-%5B%3AHAS_DATE%5D-%3E%28d%3Adim_date%29%0AWHERE%20d.year%20%3D%20%222022%22%20AND%20d.month%20%3D%20%224%22%0AWITH%20%0A%20%20%20%20p.SKU%20AS%20SKU%2C%0A%20%20%20%20p.Category%20AS%20category%2C%0A%20%20%20%20p.Size%20AS%20size%2C%0A%20%20%20%20p.Style%20AS%20style%2C%0A%20%20%20%20f.Sales_Channel_%20AS%20sales_channel%2C%0A%20%20%20%20SUM%28toFloat%28fs.amount%29%29%20AS%20total_gross_sales%0ARETURN%20%0A%20%20%20%20SKU%2C%0A%20%20%20%20category%2C%0A%20%20%20%20size%2C%0A%20%20%20%20style%2C%0A%20%20%20%20sales_channel%2C%0A%20%20%20%20total_gross_sales%0AORDER%20BY%20total_gross_sales%20DESC%0ALIMIT%2010%3B",
  },

  {
    text: "What are the total sales by order status?",
    category: "Sales Performance",
    queryUrl:
      "http://localhost:5000/analytics?DB=neo4j&query=MATCH%20%28fs%3Afact_sales%29-%5B%3AHAS_STATUS%5D-%3E%28os%3Adim_status%29%0AWITH%20%0A%20%20%20%20os.status_name%20AS%20order_status%2C%0A%20%20%20%20COUNT%28fs.order_id%29%20AS%20total_orders%2C%0A%20%20%20%20SUM%28toFloat%28fs.amount%29%29%20AS%20total_sales%0ARETURN%20%0A%20%20%20%20order_status%2C%0A%20%20%20%20total_orders%2C%0A%20%20%20%20total_sales%0AORDER%20BY%20total_sales%20DESC%3B",
  },
  {
    text: "What is the total number of orders and gross sales revenue for each order status?",
    category: "Sales Performance",
    queryUrl:
      "http://localhost:5000/analytics?DB=neo4j&query=MATCH%20%28fs%3Afact_sales%29-%5B%3AHAS_DATE%5D-%3E%28d%3Adim_date%29%0AWITH%20%0A%20%20%20%20d.year%20AS%20year%2C%0A%20%20%20%20d.month%20AS%20month%2C%0A%20%20%20%20SUM%28toFloat%28fs.amount%29%29%20AS%20total_monthly_sales%0ARETURN%20%0A%20%20%20%20month%2C%0A%20%20%20%20year%2C%0A%20%20%20%20total_monthly_sales%0AORDER%20BY%20year%2C%20month%3B",
  },
  {
    text: "Which top 5 product sizes are the most frequently ordered among items that have been shipped?",
    category: "Inventory & Product Analysis",
    queryUrl:
      "http://localhost:5000/analytics?DB=neo4j&query=MATCH%20%28fs%3Afact_sales%29-%5B%3AHAS_PRODUCT%5D-%3E%28p%3Adim_product%29%2C%0A%20%20%20%20%20%20%28fs%29-%5B%3AHAS_STATUS%5D-%3E%28os%3Adim_status%29%0AWHERE%20os.status_name%20STARTS%20WITH%20%27Shipped%27%0AWITH%20%0A%20%20%20%20p.Size%20AS%20size%2C%0A%20%20%20%20COUNT%28fs.order_id%29%20AS%20total_shipped_orders%0ARETURN%20%0A%20%20%20%20size%2C%0A%20%20%20%20total_shipped_orders%0AORDER%20BY%20total_shipped_orders%20DESC%0ALIMIT%205%3B",
  },
  {
    text: "Which top 10 products generated the highest total gross sales revenue across all time?",
    category: "Inventory & Product Analysis",
    queryUrl:
      "http://localhost:5000/analytics?DB=neo4j&query=MATCH%20%28fs%3Afact_sales%29-%5B%3AHAS_PRODUCT%5D-%3E%28p%3Adim_product%29%0AWITH%20%0A%20%20%20%20p.SKU%20AS%20SKU%2C%0A%20%20%20%20p.Category%20AS%20category%2C%0A%20%20%20%20p.Size%20AS%20size%2C%0A%20%20%20%20p.Style%20AS%20style%2C%0A%20%20%20%20SUM%28toFloat%28fs.amount%29%29%20AS%20total_revenue%0ARETURN%20%0A%20%20%20%20SKU%2C%0A%20%20%20%20category%2C%0A%20%20%20%20size%2C%0A%20%20%20%20style%2C%0A%20%20%20%20total_revenue%0AORDER%20BY%20total_revenue%20DESC%0ALIMIT%2010%3B%0A",
  },
  {
    text: "What is the total sales distribution across product categories, based on gross revenue and order volume?",
    category: "Inventory & Product Analysis",
    queryUrl:
      "http://localhost:5000/analytics?DB=neo4j&query=MATCH%20%28fs%3Afact_sales%29-%5B%3AHAS_PRODUCT%5D-%3E%28p%3Adim_product%29%0AWITH%20%0A%20%20%20%20p.Category%20AS%20category%2C%0A%20%20%20%20COUNT%28fs.order_id%29%20AS%20total_orders%2C%0A%20%20%20%20SUM%28toFloat%28fs.amount%29%29%20AS%20total_revenue%0ARETURN%20%0A%20%20%20%20category%2C%0A%20%20%20%20total_orders%2C%0A%20%20%20%20total_revenue%0AORDER%20BY%20total_revenue%20DESC%3B%0A",
  },
];

const Neo4JPage = () => {
  return (
    <div>
      <Header />
      <h1 className="text-3xl font-bold text-center mt-6">
        Welcome to Neo4J Page
      </h1>
      <QueryList queries={neo4jQueries} />
    </div>
  );
};

export default Neo4JPage;