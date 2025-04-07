import React, { useState } from "react";
import { useLocation } from "react-router-dom";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";
import TablePagination from "@mui/material/TablePagination";
import "../styles/result.css";

const ResultPage = () => {
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);

  // Pagination state
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);

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

  // Pagination handlers
  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const renderTable = () => {
    if (!data || data.length === 0) return <p>No data received</p>;

    const headers = Object.keys(data[0]);

    const capitalizedHeaders = headers.map((header) =>
      header
        .split("_")
        .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
        .join(" ")
    );

    // Slice the data for current page
    const currentPageData = data.slice(
      page * rowsPerPage,
      page * rowsPerPage + rowsPerPage
    );

    return (
      <Paper>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                {headers.map((header, index) => (
                  <TableCell
                    key={header}
                    sx={{
                      fontWeight: "bold",
                      backgroundColor: "#1976d2",
                      color: "white",
                      fontSize: "1.25rem",
                      textTransform: "capitalize",
                    }}
                  >
                    {capitalizedHeaders[index]}
                  </TableCell>
                ))}
              </TableRow>
            </TableHead>
            <TableBody>
              {currentPageData.map((row, rowIndex) => (
                <TableRow key={rowIndex}>
                  {headers.map((header) => (
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
        <TablePagination
          rowsPerPageOptions={[5, 10, 25, 50, 100]}
          component="div"
          count={data.length}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={handleChangePage}
          onRowsPerPageChange={handleChangeRowsPerPage}
        />
      </Paper>
    );
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h2>Query Result</h2>
      <p>
        <strong>Query:</strong>
        <span className="query-text">{query}</span>
      </p>
      {renderTable()}
    </div>
  );
};

export default ResultPage;
