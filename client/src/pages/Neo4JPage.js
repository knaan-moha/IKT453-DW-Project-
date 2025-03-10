import Header from "../components/Header";
import QueryList from "../components/QueryList";

const neo4jQueries = [
    { text: "MATCH (c:Customer)-[:BOUGHT]->(p:Product) RETURN c, p", category: "Market Trends" },
    { text: "MATCH (o:Order) WHERE o.status = 'returned' RETURN COUNT(o)", category: "Returns" }
  ];

const Neo4JPage = () => {
  return (
    <div>
      <Header />
      <h1 className="text-3xl font-bold text-center mt-6">Welcome to Neo4J Page</h1>
      <QueryList queries={neo4jQueries} dbType="neo4j" />
    </div>
  );
};

export default Neo4JPage;
