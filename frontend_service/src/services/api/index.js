import Axios from "axios";
import { useAuth, USER_TOKEN } from "../../contexts/Auth";
import { loadProgressBar } from "axios-progress-bar";
import { useEffect } from "react";
import { useState } from "react";
import { errorToast } from "../../help";

const authAxios = Axios.create({
  baseURL: "http://127.0.0.1:5001/auth",
});
const uploadAxios = Axios.create({
  baseURL: "http://127.0.0.1:5002/upload",
});
const reportAxios = Axios.create({
  baseURL: "http://127.0.0.1:5004/report",
});

export const AxiosInterceptor = () => {
  const { auth, logout } = useAuth();
  const [authLogout, setAuthLogout] = useState("");

  useEffect(() => {
    if (authLogout) {
      setAuthLogout("");
      logout(USER_TOKEN);
    }
  }, [authLogout]);

  useEffect(() => {
    const authReqInterceptor = authAxios.interceptors.request.use(
      (config) => {
        config.headers.Authorization = `Bearer ${auth[USER_TOKEN]}`;

        return config;
      },
      (error) => Promise.reject(error)
    );
    const authResInterceptor = authAxios.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response.status === 401) {
          setAuthLogout(error.response.data?.message ?? "unknown");
        }

        return Promise.reject(error);
      }
    );

    const uploadReqInterceptor = uploadAxios.interceptors.request.use(
      (config) => {
        config.headers.Authorization = `Bearer ${auth[USER_TOKEN]}`;

        return config;
      },
      (error) => Promise.reject(error)
    );
    const uploadResInterceptor = uploadAxios.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response.status === 401) {
          setAuthLogout(error.response.data?.message ?? "unknown");
        }

        return Promise.reject(error);
      }
    );

    return () => {
      authAxios.interceptors.request.eject(authReqInterceptor);
      authAxios.interceptors.response.eject(authResInterceptor);

      uploadAxios.interceptors.request.eject(uploadReqInterceptor);
      uploadAxios.interceptors.response.eject(uploadResInterceptor);
    };
  }, [auth]);

  return null;
};

loadProgressBar("", authAxios);
loadProgressBar("", uploadAxios);

export const authLoginRegisterAPI = ({ username, password }) =>
  authAxios.post("/login_register", {
    username,
    password,
  });
export const authLogoutAPI = () => authAxios.post("/logout");

export const uploadAPI = ({ formData }) => uploadAxios.post("/", formData);

export const reportAPI = ({ id }) => reportAxios.get(`/${id}`);
