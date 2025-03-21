from neo4j import GraphDatabase
import pandas as pd
import os
import re
from dotenv import load_dotenv

# Load .env config
load_dotenv()

neo4j_uri = os.getenv("NEO4J_URI")
neo4j_user = os.getenv("NEO4J_USER")
neo4j_password = os.getenv("NEO4J_PASSWORD")
database_name = "neo4j" 
driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

# Folder containing CSV files
csv_directory = "Data"
batch_size = 1000

# Get all CSV files
csv_files = [f for f in os.listdir(csv_directory) if f.endswith('.csv')]

# Process each CSV file
for file in csv_files:
    file_path = os.path.join(csv_directory, file)
    print(f"\n📥 Processing: {file}...")

    try:
        df = pd.read_csv(file_path, dtype=str, low_memory=False)

        # Clean column names
        df.columns = [re.sub(r'[^a-zA-Z0-9_]', '_', col.strip()) for col in df.columns]

        # Handle "Amount" column if it exists
        if "Amount" in df.columns:
            df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
            df = df.dropna(subset=["Amount"])

        # Extract label from file name
        node_label = re.sub(r'[^a-zA-Z0-9_]', '_', os.path.splitext(file)[0])
        col_names = df.columns.tolist()

        total_rows = len(df)
        for i in range(0, total_rows, batch_size):
            batch_df = df.iloc[i:i + batch_size]
            batch_data = batch_df.to_dict(orient="records")

            with driver.session(database=database_name) as session:
                for row in batch_data:
                    # Skip NaN values
                    clean_row = {k: v for k, v in row.items() if pd.notna(v)}
                    properties = ", ".join([f"{k}: ${k}" for k in clean_row])
                    query = f"CREATE (:{node_label} {{{properties}}})"
                    session.run(query, clean_row)

        print(f"✅ Finished uploading {total_rows} rows to label `{node_label}`")

    except Exception as e:
        print(f"❌ Error processing {file}: {e}")

# Close Neo4j connection
driver.close()
print("\n🎉 All CSV files successfully uploaded to Neo4j!")