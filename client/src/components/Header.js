import { Link } from "react-router-dom";
import '../styles/Header.css'

const Header = () => {
  return (
    <header>
      <nav>
        <ul>
          <li><Link to="/" className="hover:underline">MySQL</Link></li>
          <li><Link to="/mongodb" className="hover:underline">MongoDB</Link></li>
          <li><Link to="/neo4j" className="hover:underline">Neo4J</Link></li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;
