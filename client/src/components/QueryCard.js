import React from "react";
import { useNavigate } from "react-router-dom";
import "../styles/QueryCard.css";

const QueryCard = ({ text, category, dbType }) => {
    const navigate = useNavigate();

    const handleClick = async () => {
        console.log("Clicked")
        try {
            const response = await fetch(`http://localhost:5000/test?db=${dbType}`, {
                method: "GET",
            });
            
            
            if (!response.ok) {
                throw new Error("Failed to fetch data");
            }

            const result = await response.json(); // Assuming response is JSON
            console.log("meh\n",result)

            // Navigate to ResultPage with query, dbType, and fetched result
            navigate(`/result?query=${encodeURIComponent(text)}&db=${dbType}&data=${encodeURIComponent(JSON.stringify(result))}`);
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    };

    return (
        <div className="queryCard" onClick={handleClick} style={{ cursor: "pointer" }}>
            <span className="category-tag">{category}</span>
            <p className="query-text">{text}</p>
        </div>
    );
};

export default QueryCard;
