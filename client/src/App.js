import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import MySQLPage from "./pages/MySQLPage";
import MongoDBPage from "./pages/MongoDBPage";
import Neo4JPage from "./pages/Neo4JPage";
import ResultPage from "./pages/ResultPage";

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<MySQLPage />} />
        <Route path="/mongodb" element={<MongoDBPage />} />
        <Route path="/neo4j" element={<Neo4JPage />} />
        <Route path="/result" element={<ResultPage />} />
      </Routes>
    </Router>
  );
};

export default App;
