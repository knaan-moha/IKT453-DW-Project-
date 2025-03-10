import Header from "../components/Header";
import QueryList from "../components/QueryList";

const mongoQueries = [
    { text: "{ category: 'Electronics' }", category: "Product Analysis" },
    { text: "{ region: 'Europe' }", category: "Customer Insights" }
];

const MongoDBPage = () => {
  return (
    <div>
      <Header />
      <h1 className="text-3xl font-bold text-center mt-6">Welcome to MongoDB Page</h1>
      <QueryList queries={mongoQueries} dbType="mongo" />
    </div>
  );
};

export default MongoDBPage;
