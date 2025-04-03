import React from "react";
import { useLocation } from "react-router-dom";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";

const ResultPage = () => {
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const formatINR = (value) =>
    new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency: "INR",
      maximumFractionDigits: 3,
    }).format(value);

  const moneyKeywords = ["sales", "revenue", "amount", "spent"];
  const query = queryParams.get("query");
  const data = queryParams.get("data")
    ? JSON.parse(decodeURIComponent(queryParams.get("data")))
    : null;

  const renderTable = () => {
    if (!data || data.length === 0) return <p>No data received</p>;

    const headers = Object.keys(data[0]);

    return (
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              {headers.map((header) => (
                <TableCell
                  key={header}
                  sx={{
                    fontWeight: "bold",
                    backgroundColor: "#1976d2",
                    color: "white",
                  }}
                >
                  {header}
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {data.map((row, rowIndex) => (
              <TableRow key={rowIndex}>
                {headers.map((header) => (
                  //Here we can same format if we do not need  to use the indian currency
                  //<TableCell key={header}>{row[header]}</TableCell>
                  <TableCell key={header}>
                    {typeof row[header] === "number" &&
                    moneyKeywords.some((keyword) =>
                      header.toLowerCase().includes(keyword)
                    )
                      ? formatINR(row[header])
                      : row[header]}
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    );
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h2>Query Result</h2>
      <p>
        <strong>Query:</strong> {query}
      </p>
      {renderTable()}
    </div>
  );
};

export default ResultPage;
