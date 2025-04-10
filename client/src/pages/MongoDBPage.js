import Header from "../components/Header";
import QueryList from "../components/QueryList";

const mongoQueries = [
  {
    text: `What are the top 10 product category and sales channel combinations by monthly sales revenue?`,
    category: "Customer & Market Insights",
    queryUrl:
      "http://localhost:5000/analytics/mongodb/?pipeline=[%20{%20%22$group%22:%20{%20%22_id%22:%20{%20%22year%22:%20%22$date.year%22,%20%22month%22:%20%22$date.month%22,%20%22category%22:%20%22$product.Category%22,%20%22sales_channel%22:%20%22$fulfillment.Sales_Channel_%22%20},%20%22monthly_sales%22:%20{%20%22$sum%22:%20%22$amount%22%20}%20}%20},%20{%20%22$sort%22:%20{%20%22monthly_sales%22:%20-1%20}%20},%20{%20%22$limit%22:%2010%20},%20{%20%22$project%22:%20{%20%22_id%22:%200,%20%22year%22:%20%22$_id.year%22,%20%22month%22:%20%22$_id.month%22,%20%22category%22:%20%22$_id.category%22,%20%22sales_channel%22:%20%22$_id.sales_channel%22,%20%22monthly_sales%22:%201%20}%20}%20]",
  },
  {
  text: "Who are the top 10 most loyal or active customers based on the number of orders?",
  category: "Customer & Market Insights",
  queryUrl: `http://localhost:5000/analytics/mongodb/?pipeline=
    [
      {
        "$group": {
          "_id": "$customer_id",
          "total_orders": { "$sum": 1 },
          "total_spent": { "$sum": "$amount" }
        }
      },
      {
        "$sort": { "total_orders": -1 }
      },
      {
        "$limit": 10
      },
      {
        "$project": {
          "_id": 0,
          "customer_id": "$_id",
          "total_orders": 1,
          "total_spent": { "$round": ["$total_spent", 3] }
        }
      }
    ]`
  },

  {
  text: "What is the distribution of cancelled and returned orders by status type?",
  category: "Operational Efficiency",
  queryUrl: `http://localhost:5000/analytics/mongodb/?pipeline=
    [
      {
        "$match": {
          "status": {
            "$in": [
              "Cancelled",
              "Shipped - Returned to Seller",
              "Shipped - Rejected by Buyer",
              "Shipped - Lost in Transit",
              "Shipped - Returning to Seller",
              "Shipped - Damaged"
            ]
          }
        }
      },
      {
        "$group": {
          "_id": "$status",
          "total_orders": { "$sum": 1 }
        }
      },
      {
        "$sort": { "total_orders": -1 }
      },
      {
        "$project": {
          "_id": 0,
          "order_status": "$_id",
          "total_orders": 1
        }
      }
    ]`
  },
  {
  text: `What is the total gross sales revenue generated in April 2022 across all channels and products?`,
  category: "Sales Performance",
  queryUrl: "http://localhost:5000/analytics/mongodb/?pipeline=[%20{%20%22$match%22:%20{%20%22date.year%22:%202022,%20%22date.month%22:%204%20}%20},%20{%20%22$group%22:%20{%20%22_id%22:%20{%20%22SKU%22:%20%22$product.SKU%22,%20%22Category%22:%20%22$product.Category%22,%20%22Size%22:%20%22$product.Size%22,%20%22Style%22:%20%22$product.Style%22,%20%22Sales_Channel_%22:%20%22$fulfillment.Sales_Channel_%22%20},%20%22total_gross_sales%22:%20{%20%22$sum%22:%20%22$amount%22%20}%20}%20},%20{%20%22$sort%22:%20{%20%22total_gross_sales%22:%20-1%20}%20},%20{%20%22$limit%22:%2010%20},%20{%20%22$project%22:%20{%20%22_id%22:%200,%20%22Category%22:%20%22$_id.Category%22,%20%22SKU%22:%20%22$_id.SKU%22,%20%22Size%22:%20%22$_id.Size%22,%20%22Style%22:%20%22$_id.Style%22,%20%22Sales_Channel_%22:%20%22$_id.Sales_Channel_%22,%20%22Total_Sales%22:%20%22$total_gross_sales%22%20}%20}%20]"
  },
  {
    text: `Which top 10 SKUs generated the highest gross sales revenue in April 2022, considering their category, size, style, and sales channel?`,
    category: "Sales Performance",
    queryUrl: "http://localhost:5000/analytics/mongodb/?pipeline=[%20{%20%22$match%22:%20{%20%22date.year%22:%202022,%20%22date.month%22:%204%20}%20},%20{%20%22$group%22:%20{%20%22_id%22:%20{%20%22SKU%22:%20%22$product.SKU%22,%20%22Category%22:%20%22$product.Category%22,%20%22Size%22:%20%22$product.Size%22,%20%22Style%22:%20%22$product.Style%22,%20%22Sales_Channel_%22:%20%22$fulfillment.Sales_Channel_%22%20},%20%22total_gross_sales%22:%20{%20%22$sum%22:%20%22$amount%22%20}%20}%20},%20{%20%22$sort%22:%20{%20%22total_gross_sales%22:%20-1%20}%20},%20{%20%22$limit%22:%2010%20},%20{%20%22$project%22:%20{%20%22_id%22:%200,%20%22SKU%22:%20%22$_id.SKU%22,%20%22Category%22:%20%22$_id.Category%22,%20%22Size%22:%20%22$_id.Size%22,%20%22Style%22:%20%22$_id.Style%22,%20%22Sales_Channel_%22:%20%22$_id.Sales_Channel_%22,%20%22total_gross_sales%22:%201%20}%20}%20]"
  },
  {
    text: `What are the total sales by order status?`,
    category: "Sales Performance",
    queryUrl: "http://localhost:5000/analytics/mongodb/?pipeline=[{%22$group%22:{%22_id%22:%22$status%22,%22total_orders%22:{%22$sum%22:1},%22total_sales%22:{%22$sum%22:%22$amount%22}}},{%22$project%22:{%22order_status%22:%22$_id%22,%22total_orders%22:1,%22total_sales%22:1,%22_id%22:0}},{%22$sort%22:{%22total_sales%22:-1}}]"
  },
  {
    text: `What is the total number of orders and gross sales revenue for each order status?`,
    category: "Sales Performance",
    queryUrl: "http://localhost:5000/analytics/mongodb/?pipeline=[{\"$match\":{\"date.year\":{\"$exists\":true},\"date.month\":{\"$exists\":true}}},{\"$group\":{\"_id\":{\"year\":\"$date.year\",\"month\":\"$date.month\"},\"total_monthly_sales\":{\"$sum\":\"$amount\"}}},{\"$sort\":{\"_id.year\":1,\"_id.month\":1}},{\"$project\":{\"_id\":0,\"year\":\"$_id.year\",\"month\":\"$_id.month\",\"total_monthly_sales\":1}}]"
  },

  {
    text: `Which top 5 product sizes are the most frequently ordered among items that have been shipped?`,
    category: "Inventory & Product Analysis",
    queryUrl: "http://localhost:5000/analytics/mongodb/?pipeline=[{\"$match\":{\"status\":{\"$regex\":\"^Shipped\",\"$options\":\"i\"},\"product.Size\":{\"$ne\":null},\"quantity\":{\"$gt\":0}}},{\"$group\":{\"_id\":\"$product.Size\",\"totalQuantity\":{\"$sum\":\"$quantity\"}}},{\"$sort\":{\"totalQuantity\":-1}},{\"$limit\":5}]"
  },
  {
    text: `Which top 10 products generated the highest total gross sales revenue across all time?`,
    category: "Inventory & Product Analysis",
    queryUrl: "http://localhost:5000/analytics/mongodb/?pipeline=[{\"$group\":{\"_id\":{\"SKU\":\"$product.SKU\",\"Category\":\"$product.Category\",\"Size\":\"$product.Size\",\"Style\":\"$product.Style\"},\"total_revenue\":{\"$sum\":\"$amount\"}}},{\"$sort\":{\"total_revenue\":-1}},{\"$limit\":10},{\"$project\":{\"_id\":0,\"SKU\":\"$_id.SKU\",\"Category\":\"$_id.Category\",\"Size\":\"$_id.Size\",\"Style\":\"$_id.Style\",\"total_revenue\":1}}]"
  },
  {
    text: `What is the total sales distribution across product categories, based on gross revenue and order volume?`,
    category: "Inventory & Product Analysis",
    queryUrl: "http://localhost:5000/analytics/mongodb/?pipeline=[{\"$group\":{\"_id\":\"$product.Category\",\"total_orders\":{\"$sum\":1},\"total_revenue\":{\"$sum\":\"$amount\"}}},{\"$sort\":{\"total_revenue\":-1}}]"
  },
];

const MongoDBPage = () => {
  return (
    <div>
      <Header />
      <h1 className="text-3xl font-bold text-center mt-6">Welcome to MongoDB Page !</h1>
      <QueryList queries={mongoQueries} dbType="mongo" />
    </div>
  );
};

export default MongoDBPage;
