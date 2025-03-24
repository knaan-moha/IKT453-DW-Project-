import React from "react";
import { useLocation } from "react-router-dom";

const ResultPage = () => {
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);

    const query = queryParams.get("query");
    const data = queryParams.get("data") ? JSON.parse(decodeURIComponent(queryParams.get("data"))) : null;

    // Render the data as rows in a table
    const renderRows = () => {
        if (!data) return <p>No data received</p>;

        const result = data || [];

        return (
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                    </tr>
                </thead>
                <tbody>
                    {result.map((row, index) => (
                        <tr key={index}>
                            {/* Display the 'name' attribute from the row */}
                            <td>{row.n ? row.n.name : row.name}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        );
    };

    return (
        <div>
            <h2>Query Result</h2>
            <p><strong>Query:</strong> {query}</p>
            {/* <div>
                {renderRows()}
            </div> */}
            <pre>{JSON.stringify(data, null, 2)}</pre>
        </div>
    );
};

export default ResultPage;
