import React from "react";
import { useAuth, USER_TOKEN } from "../contexts/Auth";
import { Route, Redirect } from "react-router-dom";

const ProtectedRoute = (props) => {
  const { auth } = useAuth();

  if (auth[USER_TOKEN]) {
    return <Route {...props} />;
  } else {
    return <Redirect to="/login-register" />;
  }
};

export default ProtectedRoute;
