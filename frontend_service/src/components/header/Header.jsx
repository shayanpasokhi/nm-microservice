import React from "react";
import CustomStepper from "../stepper/CustomStepper";
import Box from "@mui/material/Box";
import indexRoutes from "../../routes";

const Header = (props) => {
  const stepperRoutes = indexRoutes
    .find((route) => route.path == "/")
    .routes.filter((route) => route.showInStepper);

  const stepperSteps = stepperRoutes.map((route) => route.name);
  const stepperIcons = stepperRoutes.map((route) => route.icon);
  const stepperActiveStep = stepperRoutes
    .map((route) => route.path)
    .indexOf(props.location.pathname);

  return (
    <Box
      sx={{
        width: 1,
      }}
    >
      <CustomStepper
        activeStep={stepperActiveStep}
        steps={stepperSteps}
        icons={stepperIcons}
      />
    </Box>
  );
};

export default Header;
