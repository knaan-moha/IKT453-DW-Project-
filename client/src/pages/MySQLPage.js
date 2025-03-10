import Header from "../components/Header";
import QueryList from "../components/QueryList";

const MySQLPage = () => {
  return (
    <div>
      <Header />
      <h1 className="text-3xl font-bold text-center mt-6">Welcome to MySQL Page</h1>
      <QueryList />
    </div>
  );
};

export default MySQLPage;
