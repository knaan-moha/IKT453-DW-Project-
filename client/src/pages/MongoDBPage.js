import Header from "../components/Header";
import QueryList from "../components/QueryList";

const MongoDBPage = () => {
  return (
    <div>
      <Header />
      <h1 className="text-3xl font-bold text-center mt-6">Welcome to MongoDB Page</h1>
      <QueryList />
    </div>
  );
};

export default MongoDBPage;
