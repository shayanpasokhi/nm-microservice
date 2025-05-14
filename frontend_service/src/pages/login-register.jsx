import TextField from "@mui/material/TextField";
import Box from "@mui/material/Box";
import logo from "../assets/images/logo.png";
import Typography from "@mui/material/Typography";
import { useForm, Controller } from "react-hook-form";
import {
  requiredValidation,
  errorToast,
  successToast,
  extractErrorMessage,
} from "../help";
import LoadingButton from "@mui/lab/LoadingButton";
import { useAuth, USER_TOKEN } from "../contexts/Auth";
import { useEffect, useState } from "react";
import { useHistory } from "react-router-dom";
import { authLoginRegisterAPI } from "../services/api";
import Alert from "@mui/material/Alert";

function Copyright(props) {
  return (
    <Typography
      variant="body2"
      color="text.secondary"
      align="center"
      {...props}
    >
      {"Copyright © FScan "}
      {new Date().getFullYear()}
    </Typography>
  );
}

const LoginRegisterPage = () => {
  const { auth, login } = useAuth();
  const [error, setError] = useState("");
  const {
    formState: { errors, isSubmitting },
    control,
    handleSubmit,
  } = useForm({
    mode: "all",
    shouldUnregister: true,
    defaultValues: {
      username: "",
      password: "",
    },
  });
  const history = useHistory();

  useEffect(() => {
    if (auth[USER_TOKEN]) {
      history.push("/");
    }
  }, [auth]);

  const onSubmit = (data) =>
    authLoginRegisterAPI({
      username: data.username,
      password: data.password,
    })
      .then(({ data }) => {
        if (data?.access_token) {
          login(data.access_token, USER_TOKEN);
          history.push("/");
          successToast(data?.msg ?? "");
        } else {
          setError(() => data?.msg ?? "خطا!");
        }
      })
      .catch((err) => {
        const msg = extractErrorMessage(err);
        errorToast(msg);
      });

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
      <Box
        sx={{ display: "flex", justifyContent: "center", alignItems: "center" }}
      >
        <Box
          sx={{ width: "150px", objectFit: "contain" }}
          component="img"
          src={logo}
          alt="لوگوی FScan"
        />
      </Box>
      {error && <Alert severity="error">{error}</Alert>}
      <Box component="form" onSubmit={handleSubmit(onSubmit)}>
        <Controller
          control={control}
          name="username"
          render={({ field }) => (
            <TextField
              {...field}
              margin="normal"
              fullWidth
              id="username"
              label="نام کاربری"
              name="username"
              error={!!errors.username}
              helperText={errors.username?.message}
            />
          )}
          rules={{
            ...requiredValidation,
          }}
        />
        <Controller
          control={control}
          name="password"
          render={({ field }) => (
            <TextField
              {...field}
              margin="normal"
              fullWidth
              id="password"
              label="رمز عبور"
              name="password"
              type="password"
              error={!!errors.password}
              helperText={errors.password?.message}
            />
          )}
          rules={{
            ...requiredValidation,
          }}
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
        >
          ورود
        </LoadingButton>
        <Copyright sx={{ my: 2 }} />
      </Box>
    </Box>
  );
};

export default LoginRegisterPage;
