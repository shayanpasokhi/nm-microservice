import Box from "@mui/material/Box";
import Divider from "@mui/material/Divider";
import Chip from "@mui/material/Chip";
import DoneIcon from "@mui/icons-material/Done";
import CloseIcon from "@mui/icons-material/Close";
import CircularProgress from "@mui/material/CircularProgress";
import PriorityHighIcon from "@mui/icons-material/PriorityHigh";

const fileStatusInfo = {
  in_progress: {
    icon: <CircularProgress size={23} />,
    color: "default",
    variant: "outlined",
  },
  not_infected: { icon: <DoneIcon />, color: "success", variant: "outlined" },
  infected: { icon: <CloseIcon />, color: "error", variant: "outlined" },
  error: { icon: <PriorityHighIcon />, color: "warning", variant: "outlined" },
};

const ScanReport = ({ imgSrc, name, report }) => {
  return (
    <Box
      sx={{
        border: "1px solid",
        borderColor: "#bbb",
        width: 1,
        maxWidth: 1,
        height: "85px",
        minHeight: "85px",
        borderRadius: 5,
        p: 2,
        my: 2,
        display: "flex",
        alignItems: "center",
        overflow: "auto",
      }}
    >
      <Box
        sx={{
          width: "100px",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <Box
          sx={{
            width: "40px",
            height: "40px",
            objectFit: "contain",
          }}
          component="img"
          src={imgSrc}
        />
      </Box>
      <Divider
        orientation="vertical"
        flexItem
        sx={{ borderColor: "#bbb", mx: 2 }}
      />
      <Box
        sx={{
          width: "150px",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontSize: 20,
        }}
      >
        {name}
      </Box>
      <Divider
        orientation="vertical"
        flexItem
        sx={{ borderColor: "#bbb", mx: 2 }}
      />
      <Box
        sx={{
          flex: 1,
          display: "flex",
          alignItems: "center",
          overflowX: "auto",
          minWidth: "100px",
        }}
      >
        {report.map((file, index) => (
          <Chip
            key={index}
            sx={{ fontSize: 15, mr: 2 }}
            icon={fileStatusInfo?.[file?.scan_status ?? ""]?.icon ?? ""}
            color={
              fileStatusInfo?.[file?.scan_status ?? ""]?.color ?? "default"
            }
            variant={fileStatusInfo?.[file?.scan_status ?? ""]?.variant ?? "outlined"}
            label={file?.files_name ?? ""}
          />
        ))}
      </Box>
    </Box>
  );
};

export default ScanReport;
