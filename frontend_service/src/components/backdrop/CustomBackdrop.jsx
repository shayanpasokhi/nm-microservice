import Backdrop from "@mui/material/Backdrop";
import CircularProgress from "@mui/material/CircularProgress";
import LinearProgress from "@mui/material/LinearProgress";
import Box from "@mui/material/Box";
import logo from "../../assets/images/logo.png";
import Typography from "@mui/material/Typography";

const CustomBackdrop = ({ open, des = "لطفا صبر کنید…" }) => {
  return (
    <Backdrop sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }} open={open}>
      <Box
        sx={{
          minWidth: 250,
          backgroundColor: "#fff",
          borderRadius: 5,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          flexDirection: "column",
        }}
      >
        <Box
          sx={{ width: "100px", objectFit: "contain", mt: 2 }}
          component="img"
          src={logo}
          alt="لوگوی FScan"
        />
        {des && (
          <Typography
            variant="body2"
            sx={{ wordWrap: "anywhere", mt: 2 }}
            color="text.secondary"
          >
            {des}
          </Typography>
        )}
        <LinearProgress sx={{ width: "90%", my: 2 }} />
      </Box>
    </Backdrop>
  );
};

export default CustomBackdrop;
