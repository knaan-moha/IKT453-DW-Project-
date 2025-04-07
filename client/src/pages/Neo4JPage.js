import Header from "../components/Header";
import QueryList from "../components/QueryList";

const neo4jQueries = [
  {
    text: "Get all data from test table",
    category: "Test Query 1",
    queryUrl:
      "http://localhost:5000/analytics?DB=neo4j&query=MATCH%20(n)%20RETURN%20n",
  },
  {
    text: "Get data from test table given id",
    category: "Test Query 2",
    queryUrl:
      "http://localhost:5000/analytics?DB=neo4j&query=MATCH%20(p:Person%20{name:%20$1})%20RETURN%20p&params=Alice",
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
