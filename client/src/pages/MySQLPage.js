import Header from "../components/Header";
import QueryList from "../components/QueryList";

const mysqlQueries = [
  { text: "SELECT * FROM sales WHERE month = 'January'", category: "Sales Performance" },
  { text: "SELECT COUNT(*) FROM orders WHERE status = 'cancelled'", category: "Operational Efficiency" }
];

const MySQLPage = () => {
  return (
    <div>
      <Header />
      <h1 className="text-3xl font-bold text-center mt-6">Welcome to MySQL Page</h1>
      <QueryList queries={mysqlQueries} dbType="mysql" />
    </div>
  );
};

export default MySQLPage;
