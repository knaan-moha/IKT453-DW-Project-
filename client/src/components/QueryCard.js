import React from "react";
import { useNavigate } from "react-router-dom";
import "../styles/QueryCard.css";

const QueryCard = ({ text, category, queryUrl }) => {
    const navigate = useNavigate();

    const handleClick = async () => {
        console.log("Clicked with URL:", queryUrl);
        try {
            const response = await fetch(queryUrl, {
                method: "GET",
            });

            if (!response.ok) {
                throw new Error("Failed to fetch data");
            }

            const result = await response.json(); // Assuming the response is JSON
            console.log("Fetched result:", result);

            // Navigate to ResultPage with query and fetched result
            navigate(`/result?query=${encodeURIComponent(text)}&data=${encodeURIComponent(JSON.stringify(result.result))}`);
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
