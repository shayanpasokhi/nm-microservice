import React from "react";
import { Typography, Button } from "@mui/material";
import { Link } from "react-router-dom";

const NotFound = () => {
  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <Typography variant="h1">404</Typography>
      <Typography style={{ marginTop: "25px" }} variant="h4">
        صفحه مورد نظر یافت نشد
      </Typography>
      <Button
        style={{ marginTop: "50px" }}
        variant="contained"
        component={Link}
        to="/"
      >
        رفتن به خانه
      </Button>
    </div>
  );
};

export default NotFound;
