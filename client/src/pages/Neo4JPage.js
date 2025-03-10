import Header from "../components/Header";
import QueryList from "../components/QueryList";

const Neo4JPage = () => {
  return (
    <div>
      <Header />
      <h1 className="text-3xl font-bold text-center mt-6">Welcome to Neo4J Page</h1>
      <QueryList />
    </div>
  );
};

export default Neo4JPage;
