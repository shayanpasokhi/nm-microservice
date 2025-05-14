import React, { useEffect, useState } from "react";
import {
  Box,
  Typography,
  Card,
  CardContent,
  Chip,
  Stack,
  Divider,
} from "@mui/material";
import ErrorOutlineIcon from "@mui/icons-material/ErrorOutline";
import CheckCircleOutlineIcon from "@mui/icons-material/CheckCircleOutline";
import FilePresentIcon from "@mui/icons-material/FilePresent";
import FingerprintIcon from "@mui/icons-material/Fingerprint";
import SecurityIcon from "@mui/icons-material/Security";
import AccessTimeIcon from "@mui/icons-material/AccessTime";
import CustomBackdrop from "../components/backdrop/CustomBackdrop";
import { useReport } from "../contexts/Report";
import { maxReqTryCount } from "../constants";
import { reportAPI } from "../services/api";
import { errorToast, extractErrorMessage } from "../help";
import { useHistory } from "react-router-dom";

const ScanPage = () => {
  const { report } = useReport();
  const [isLoadingReport, setIsLoadingReport] = useState(true);
  const [countFailReq, setCountFailReq] = useState(0);
  const [res, setRes] = useState({});
  const history = useHistory();

  useEffect(() => {
    getReport(report?.report_id);
  }, []);

  useEffect(() => {
    if (countFailReq >= maxReqTryCount) {
      errorToast("");
      history.push("/");
    }
  }, [countFailReq]);

  useEffect(() => {
    const ReportInterval = setInterval(() => {
      if (
        !isLoadingReport &&
        !res?.["scanned_at"] &&
        countFailReq < maxReqTryCount
      ) {
        getReport(report?.report_id);
      }
    }, 3000);

    return () => clearInterval(ReportInterval);
  }, [isLoadingReport]);

  const getReport = (id) => {
    setIsLoadingReport(true);

    reportAPI({ id: id })
      .then(({ data }) => {
        if (data?.success) {
          setRes({
            scanner: data.scanner,
            result: data.result,
            scanned_at: data.scanned_at,
            is_infected: data.is_infected,
          });
        } else {
          errorToast(data?.msg ?? "خطا در گرفتن اطلاعات!");
          setCountFailReq((pre) => pre + 1);
        }
      })
      .catch((err) => {
        const msg = extractErrorMessage(err);
        errorToast(msg);
        setCountFailReq((pre) => pre + 1);
      })
      .then(() => {
        setIsLoadingReport(false);
      });
  };

  return (
    <Box
      sx={{
        width: {
          xs: "100%",
          sm: "100%",
          md: "50%",
          lg: "33%",
        },
        display: "flex",
        flexDirection: "column",
        maxHeight: "100%",
      }}
    >
      <CustomBackdrop open={!res?.["scanned_at"]} des="در حال پویش…" />
      <Box>
        <Card
          elevation={4}
          sx={{
            borderLeft: `15px solid ${
              res?.is_infected === true
                ? "#d32f2f"
                : res?.is_infected === false
                ? "#2e7d32"
                : "#9e9e9e"
            }`,
            borderRadius: 2,
            p: 2,
          }}
        >
          <CardContent>
            <Stack spacing={2}>
              <Typography variant="h6">
                <FilePresentIcon sx={{ mr: 1, verticalAlign: "middle" }} />
                {report?.filename}
              </Typography>

              <Stack direction="row" spacing={1} alignItems="center">
                <FingerprintIcon fontSize="small" color="action" />
                <Typography
                  variant="body2"
                  color="text.secondary"
                  sx={{ wordBreak: "break-all" }}
                >
                  {report?.file_hash}
                </Typography>
              </Stack>
              <Divider />
              {res?.["scanned_at"] && (
                <>
                  <Stack direction="row" spacing={1} alignItems="center">
                    <SecurityIcon fontSize="small" color="action" />
                    <Typography variant="body2" color="text.secondary">
                      اسکنر: {res?.scanner}
                    </Typography>
                  </Stack>

                  <Box>
                    <Typography
                      variant="subtitle2"
                      color="text.secondary"
                      gutterBottom
                    >
                      نتیجه اسکن:
                    </Typography>

                    <Box
                      dir="ltr"
                      sx={{
                        bgcolor: "#f5f5f5",
                        p: 2,
                        borderRadius: 2,
                        fontFamily: "monospace",
                        fontSize: "0.875rem",
                        whiteSpace: "pre-wrap",
                        overflowX: "auto",
                        textAlign: "right",
                      }}
                    >
                      {(() => {
                        try {
                          const parsed = JSON.parse(res?.result);
                          return <pre>{JSON.stringify(parsed, null, 2)}</pre>;
                        } catch (e) {
                          return res?.result || "نامعتبر";
                        }
                      })()}
                    </Box>
                  </Box>

                  <Stack direction="row" spacing={1} alignItems="center">
                    <AccessTimeIcon fontSize="small" color="action" />
                    <Typography variant="caption" color="text.secondary">
                      زمان اسکن:{" "}
                      {new Date(res?.scanned_at).toLocaleString("fa-IR", {
                        year: "numeric",
                        month: "2-digit",
                        day: "2-digit",
                        hour: "2-digit",
                        minute: "2-digit",
                      })}
                    </Typography>
                  </Stack>

                  <Box>
                    {res?.is_infected === true ? (
                      <Chip
                        icon={<ErrorOutlineIcon />}
                        label="آلوده"
                        color="error"
                        variant="filled"
                      />
                    ) : res?.is_infected === false ? (
                      <Chip
                        icon={<CheckCircleOutlineIcon />}
                        label="سالم"
                        color="success"
                        variant="filled"
                      />
                    ) : (
                      <Chip
                        icon={<ErrorOutlineIcon />}
                        label="نامشخص"
                        sx={{ bgcolor: "#9e9e9e", color: "white" }}
                        variant="filled"
                      />
                    )}
                  </Box>
                </>
              )}
            </Stack>
          </CardContent>
        </Card>
      </Box>
    </Box>
  );
};

export default ScanPage;
