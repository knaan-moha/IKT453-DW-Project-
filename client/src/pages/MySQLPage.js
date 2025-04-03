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
