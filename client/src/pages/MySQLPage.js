import Header from "../components/Header";
import QueryList from "../components/QueryList";

const mysqlQueries = [
  { 
    text: "Get all data from test table", 
    category: "Test Query 1", 
    queryUrl: "http://localhost:5000/analytics?DB=mysql&query=SELECT%20*%20FROM%20test" 
  },
  { 
    text: "Get data from test table given id", 
    category: "Test Query 2", 
    queryUrl: "http://localhost:5000/analytics?DB=mysql&query=SELECT%20*%20FROM%20test%20WHERE%20id%20=%20%s&params=1" 
  }
];

const MySQLPage = () => {
  return (
    <div>
      <Header />
      <h1 className="text-3xl font-bold text-center mt-6">Welcome to MySQL Page</h1>
      <QueryList queries={mysqlQueries}/>
    </div>
  );
};

export default MySQLPage;
