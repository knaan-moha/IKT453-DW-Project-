import React from "react";
import "../styles/QueryCard.css";

const QueryCard = ({ text, category }) => {
  return (
    <div className="queryCard">
        <span className="category-tag">{category}</span>
        <p className="query-text">{text}</p>
    </div>
  );
};

export default QueryCard;