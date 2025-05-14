import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import { AuthProvider } from "./contexts/Auth";
import { ReportProvider } from "./contexts/Report";
import indexRoutes from "./routes";

import { BrowserRouter, Route, Switch } from "react-router-dom";
import { QueryParamProvider } from "use-query-params";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import { CacheProvider } from "@emotion/react";
import createCache from "@emotion/cache";
import { prefixer } from "stylis";
import rtlPlugin from "stylis-plugin-rtl";
import { ToastContainer } from "react-toastify";
import { css } from "@emotion/css";
import { AxiosInterceptor } from "./services/api";

import "@fontsource/roboto/300.css";
import "@fontsource/roboto/400.css";
import "@fontsource/roboto/500.css";
import "@fontsource/roboto/700.css";
import "react-toastify/dist/ReactToastify.css";
import "axios-progress-bar/dist/nprogress.css";
import "vazir-font/dist/font-face.css";

const cacheRtl = createCache({
  key: "muirtl",
  stylisPlugins: [prefixer, rtlPlugin],
});

const defaultTheme = createTheme({
  palette: {
    primary: {
      main: "#1F4E79",
      contrastText: "#ffffff",
    },
    secondary: {
      main: "#F5A623",
    },
  },
  direction: "rtl",
  typography: {
    fontFamily: "Vazir",
  },
});

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <BrowserRouter>
    <QueryParamProvider ReactRouterRoute={Route}>
      <CacheProvider value={cacheRtl}>
        <ThemeProvider theme={defaultTheme}>
          <CssBaseline />
          <AuthProvider>
            <AxiosInterceptor />
            <ToastContainer
              toastClassName={css`
                font-family: "Vazir";
              `}
              theme="colored"
              position="bottom-right"
              autoClose={5000}
              hideProgressBar={false}
              newestOnTop
              closeOnClick
              rtl
              pauseOnFocusLoss
              draggable
              pauseOnHover
            />
            <ReportProvider>
              <Switch>
                {indexRoutes.map((prop, key) => {
                  return (
                    <Route
                      path={prop.path}
                      key={key}
                      component={prop.component}
                    />
                  );
                })}
              </Switch>
            </ReportProvider>
          </AuthProvider>
        </ThemeProvider>
      </CacheProvider>
    </QueryParamProvider>
  </BrowserRouter>
);
