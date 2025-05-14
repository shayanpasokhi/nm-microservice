import Header from "../components/header/Header";
import { Box } from "@mui/material";
import Stack from "@mui/system/Stack";
import { Redirect, Route, Switch } from "react-router-dom";
import indexRoutes from "../routes";
import ProtectedRoute from "../components/ProtectedRoute";
import DefaultSpeedDial from "../components/speedDial/DefaultSpeedDial";
import { useAuth, USER_TOKEN } from "../contexts/Auth";

const DefaultLayout = (props) => {
  const { auth, logout } = useAuth();

  return (
    <Box
      sx={{
        display: "flex",
        alignItems: "center",
        flexDirection: "column",
        width: "100vw",
        height: "100vh",
        bgcolor: "#fafafa",
      }}
    >
      {auth[USER_TOKEN] && <DefaultSpeedDial />}
      <Box
        sx={{
          boxShadow: "0px 12px 24px rgba(0, 0, 0, 0.25)",
          width: "90%",
          height: "66px",
          borderRadius: 5,
          bgcolor: "background.paper",
          p: 2,
          mt: 2,
          overflow: "auto",
        }}
      >
        <Box
          sx={{
            width: 1,
            height: 1,
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <Header {...props} />
        </Box>
      </Box>
      <Box
        sx={{
          width: "90%",
          flex: 1,
          boxShadow: "0px 12px 24px rgba(0, 0, 0, 0.25)",
          borderRadius: 5,
          bgcolor: "background.paper",
          p: 2,
          my: 2,
          overflow: "auto",
        }}
      >
        <Box
          sx={{
            width: 1,
            height: 1,
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <Switch>
            {indexRoutes
              .find((route) => route.path == "/")
              .routes.map((prop, key) => {
                if (prop.redirect) {
                  return (
                    <Redirect from={prop.path} to={prop.pathTo} key={key} />
                  );
                } else if (prop.private) {
                  return <ProtectedRoute {...prop} key={key} />;
                } else {
                  return <Route {...prop} key={key} />;
                }
              })}
          </Switch>
        </Box>
      </Box>
    </Box>
  );
};

export default DefaultLayout;
