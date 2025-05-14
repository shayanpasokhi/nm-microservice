import * as React from "react";
import Box from "@mui/material/Box";
import Backdrop from "@mui/material/Backdrop";
import SpeedDial from "@mui/material/SpeedDial";
import SpeedDialIcon from "@mui/material/SpeedDialIcon";
import SpeedDialAction from "@mui/material/SpeedDialAction";
import FileCopyIcon from "@mui/icons-material/FileCopyOutlined";
import DocumentScannerIcon from "@mui/icons-material/DocumentScanner";
import LogoutIcon from "@mui/icons-material/Logout";
import { useAuth, USER_TOKEN } from "../../contexts/Auth";
import { useHistory } from "react-router-dom";

const DefaultSpeedDial = () => {
  const { auth, logout } = useAuth();
  const [open, setOpen] = React.useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);
  const history = useHistory();

  return (
    <>
      <Backdrop open={open} />
      <SpeedDial
        ariaLabel="SpeedDial tooltip example"
        sx={{ position: "absolute", bottom: 16, right: 16 }}
        icon={<SpeedDialIcon />}
        onClose={handleClose}
        onOpen={handleOpen}
        open={open}
      >
        <SpeedDialAction
          icon={<LogoutIcon />}
          tooltipTitle={"خروج"}
          tooltipOpen
          onClick={() => {
            logout(USER_TOKEN);
            handleClose();
          }}
        />
        <SpeedDialAction
          icon={<DocumentScannerIcon />}
          tooltipTitle={"پویش مجدد"}
          tooltipOpen
          onClick={() => {
            history.push("/");
            handleClose();
          }}
        />
      </SpeedDial>
    </>
  );
};

export default DefaultSpeedDial;
