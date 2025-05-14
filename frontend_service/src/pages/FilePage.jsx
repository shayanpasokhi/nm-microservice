import React, { useCallback } from "react";
import { useDropzone } from "react-dropzone";
import {
  Box,
  Typography,
  Chip,
  Checkbox,
  FormControlLabel,
} from "@mui/material";
import UploadFileIcon from "@mui/icons-material/UploadFile";
import { useForm, Controller } from "react-hook-form";
import LoadingButton from "@mui/lab/LoadingButton";
import { uploadAPI } from "../services/api";
import {
  requiredValidation,
  extractErrorMessage,
  errorToast,
  successToast,
  getSize,
} from "../help";
import { maxFileSize } from "../constants";
import { useReport } from "../contexts/Report";
import { useHistory } from "react-router-dom";

const FilePage = () => {
  const {
    handleSubmit,
    control,
    setValue,
    watch,
    formState: { isSubmitting },
  } = useForm({
    defaultValues: {
      push_req: false,
    },
  });
  const { addReport, cleanReport } = useReport();
  const history = useHistory();

  const file = watch("file");

  const onDrop = useCallback(
    (acceptedFiles) => {
      const selected = acceptedFiles[0];

      if (selected.size > maxFileSize) {
        errorToast(`حجم فایل نباید بیشتر از ${getSize(maxFileSize)} باشد.`);
        return;
      }

      setValue("file", selected, { shouldValidate: true });
    },
    [setValue]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    maxFiles: 1,
    multiple: false,
  });

  const onSubmit = (data) => {
    const formData = new FormData();
    formData.append("file", data.file);
    formData.append("push_req", data.push_req ? "true" : "false");

    return uploadAPI({ formData })
      .then(({ data }) => {
        if (
          data?.report_ids &&
          data?.file_id &&
          data?.filename &&
          data?.file_hash
        ) {
          addReport({
            file_id: data.file_id,
            filename: data.filename,
            file_hash: data.file_hash,
            report_id: data.report_ids[0],
          });
          history.push({
            pathname: "/scan",
          });
          successToast(data?.msg ?? "");
        } else {
          errorToast(() => data?.msg ?? "خطا!");
        }
      })
      .catch((err) => {
        const msg = extractErrorMessage(err);
        errorToast(msg);
      });
  };

  return (
    <Box
      component="form"
      onSubmit={handleSubmit(onSubmit)}
      sx={{
        width: { xs: "100%", sm: "100%", md: "50%", lg: "33%" },
        display: "flex",
        flexDirection: "column",
        maxHeight: "100%",
      }}
    >
      <Controller
        name="file"
        control={control}
        rules={{ ...requiredValidation }}
        render={() => (
          <Box
            {...getRootProps()}
            sx={{
              border: "2px dashed #1F4E79",
              borderRadius: 5,
              p: 4,
              bgcolor: isDragActive ? "#e3f2fd" : "#fafafa",
              cursor: "pointer",
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
              alignItems: "center",
            }}
          >
            <input {...getInputProps()} />
            <UploadFileIcon color="primary" sx={{ fontSize: 60 }} />
            <Typography align="center" variant="h6" sx={{ mt: 2 }}>
              {isDragActive
                ? "فایل خود را اینجا رها کنید..."
                : "یک فایل را در اینجا بکشید و رها کنید یا برای انتخاب کلیک کنید"}
            </Typography>
            <Typography align="center" variant="body2" color="textSecondary">
              فقط یک فایل قابل آپلود است
            </Typography>
          </Box>
        )}
      />
      {file && (
        <Box mt={2}>
          <Chip label={file.name} color="primary" variant="outlined" />
        </Box>
      )}
      <Controller
        name="push_req"
        control={control}
        render={({ field }) => (
          <FormControlLabel
            sx={{ mt: 2 }}
            control={<Checkbox {...field} checked={field.value} />}
            label="درخواست انتقال"
          />
        )}
      />
      <LoadingButton
        loading={isSubmitting}
        variant="contained"
        color="primary"
        fullWidth
        loadingIndicator="لطفا صبر کنید…"
        sx={{ mt: 3, mb: 2 }}
        type="submit"
        size="large"
        disabled={!file || isSubmitting}
      >
        بارگذاری
      </LoadingButton>
    </Box>
  );
};

export default FilePage;
