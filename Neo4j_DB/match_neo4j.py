from neo4j import GraphDatabase
import os

# Setup connection
neo4j_uri = os.getenv("NEO4J_URI")
neo4j_user = os.getenv("NEO4J_USER")
neo4j_password = os.getenv("NEO4J_PASSWORD")
database_name = "neo4j"  # Or whatever your database is called

driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

# List of MATCH queries
queries = [
    "MATCH (n:Amazon_Sale_Report) RETURN n LIMIT 25",
    "MATCH (n:dim_courier_status) RETURN n LIMIT 25",
    "MATCH (n:dim_customer) RETURN n LIMIT 25",
    "MATCH (n:dim_date) RETURN n LIMIT 25",
    "MATCH (n:dim_fulfillment) RETURN n LIMIT 25",
    "MATCH (n:dim_product) RETURN n LIMIT 25",
    "MATCH (n:dim_promotion) RETURN n LIMIT 25",
    "MATCH (n:dim_status) RETURN n LIMIT 25",
    "MATCH (n:fact_sales) RETURN n LIMIT 25",
    // ---------------------
    // Fact-Dimension Matching Queries
    // ---------------------

    // Match fact_sales to DimCustomer
    "MATCH (f:fact_sales) MATCH (c:DimCustomer {customer_id: f.customer_id}) MERGE (f)-[:HAS_CUSTOMER]->(c)",

    // Match fact_sales to dim_courier_status
    "MATCH (f:fact_sales) MATCH (cs:dim_courier_status {courier_status_id: f.courier_status_id}) MERGE (f)-[:HAS_COURIER_STATUS]->(cs)",

    // Match fact_sales to dim_date
    "MATCH (f:fact_sales) MATCH (d:dim_date {date_id: f.date_id}) MERGE (f)-[:HAS_DATE]->(d)",

    // Match fact_sales to dim_fulfillment
    "MATCH (f:fact_sales) MATCH (fu:dim_fulfillment {fulfillment_id: f.fulfillment_id}) MERGE (f)-[:HAS_FULFILLMENT]->(fu)",

    // Match fact_sales to dim_product
    "MATCH (f:fact_sales) MATCH (p:dim_product {product_id: f.product_id}) MERGE (f)-[:HAS_PRODUCT]->(p)",

    // Match fact_sales to dim_status
    "MATCH (f:fact_sales) MATCH (s:dim_status {status_id: f.status_id}) MERGE (f)-[:HAS_STATUS]->(s)"
]

# Function to run and print results
def run_queries():
    with driver.session(database=database_name) as session:
        for idx, query in enumerate(queries, start=1):
            print(f"\nRunning Query {idx}: {query}\n")
            result = session.run(query)
            for record in result:
                print(record)

# Run all
run_queries()