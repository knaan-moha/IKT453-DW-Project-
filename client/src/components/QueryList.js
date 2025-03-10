import React from "react";
import QueryCard from "./QueryCard";

const queries = [
    { text: "What is the monthly sales revenue trend for each product category and sales channel?", category: "Sales Performance" },
    { text: "Which top 5 SKUs generated the highest revenue in Q1 2022?", category: "Sales Performance" },
    { text: "What is the total gross amount for sales in January 2022?", category: "Sales Performance" },
    { text: "Will there be a higher sales volume on holidays and weekends compared to working days?", category: "Sales Performance" },
    
    { text: "Which products are low in stock but have high sales velocity?", category: "Inventory & Product Analysis" },
    { text: "Which product has the highest total sales amount across all reports?", category: "Inventory & Product Analysis" },
    { text: "Which product has never been sold in any report?", category: "Inventory & Product Analysis" },
    { text: "Which size is most popular for shipped items?", category: "Inventory & Product Analysis" },
    { text: "List the popular items that have low stock in size XL.", category: "Inventory & Product Analysis" },
  
    { text: "Who are the top 10 international customers by purchase volume?", category: "Customer & Market Insights" },
    { text: "Top 10 cities order from Amazon sorted by amount?", category: "Customer & Market Insights" },
    { text: "Which regions are experiencing the highest growth in sales?", category: "Customer & Market Insights" },
    { text: "Which customer has spent the most across all sales reports?", category: "Customer & Market Insights" },
    { text: "Which province has the highest Amazon popularity in terms of sales transactions per capita?", category: "Customer & Market Insights" },
  
    { text: "What is the profit margin per SKU when comparing Final MRP Old to TP1/TP2 prices?", category: "Pricing & Profitability" },
    { text: "How does discounting (MRP Old vs. Final MRP Old) impact the sales volume?", category: "Pricing & Profitability" },
    { text: "Will the promotion ID be helpful in increasing sales volume?", category: "Pricing & Profitability" },
  
    { text: "Which fulfillment method (e.g., FBA vs. self-fulfilled) has the lowest shipping failure rate?", category: "Operational Efficiency" },
    { text: "Calculate the number of canceled or returned orders.", category: "Operational Efficiency" }
  ];

const QueryList = () => {
  return (
    <div>
      {queries.map((query, index) => (
        <QueryCard key={index} text={query.text} category={query.category} />
      ))}
    </div>
  );
};

export default QueryList;
