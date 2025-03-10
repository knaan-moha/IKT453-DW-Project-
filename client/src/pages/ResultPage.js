import React from "react";
import { useLocation } from "react-router-dom";

const ResultPage = () => {
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);

    const query = queryParams.get("query");
    const dbType = queryParams.get("db");
    const data = queryParams.get("data") ? JSON.parse(decodeURIComponent(queryParams.get("data"))) : null;

    return (
        <div>
            <h2>Query Result</h2>
            <p><strong>Query:</strong> {query}</p>
            <p><strong>Database:</strong> {dbType}</p>
            <pre>{data ? JSON.stringify(data, null, 2) : "No data received"}</pre>
        </div>
    );
};

export default ResultPage;
