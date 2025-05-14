import React, {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useState,
  useEffect,
} from "react";
import { authLogoutAPI } from "../services/api";
import { errorToast, successToast, extractErrorMessage } from "../help";

const AuthContext = createContext(undefined);

const AUTH_KEY = "auth";
const USER_TOKEN = "userToken";

const setLocalStorage = (key, value) => {
  try {
    localStorage.setItem(key, JSON.stringify(value));
  } catch (e) {
    console.error({ e });
  }
};

const getLocalStorage = (key, initialValue) => {
  try {
    const value = localStorage.getItem(key);
    return value ? JSON.parse(value) : initialValue;
  } catch (e) {
    return initialValue;
  }
};

const AuthProvider = ({ children }) => {
  const [auth, setAuth] = useState(() =>
    getLocalStorage(AUTH_KEY, {
      [USER_TOKEN]: "",
    })
  );
  useEffect(() => {
    setLocalStorage(AUTH_KEY, auth);
  }, [auth]);

  const login = (token, key) => {
    setAuth((pre) => ({ ...pre, [key]: token }));
  };

  const logout = (key) => {
    if (auth[key]) {
      authLogoutAPI()
        .then(({ data }) => {
          if (data?.success) {
            successToast(data?.msg ?? "");
          } else {
            errorToast(data?.msg ?? "خطا!");
          }
        })
        .catch((err) => {
          const msg = extractErrorMessage(err);
          errorToast(msg);
        });
    }
    setAuth((pre) => ({ ...pre, [key]: "" }));
  };

  const value = useMemo(() => ({ auth, login, logout }), [auth, login, logout]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

const useAuth = () => {
  const context = useContext(AuthContext);

  if (context === undefined)
    throw new Error("useAuth must be within AuthProvider!");

  return context;
};

export { AuthProvider, useAuth, AUTH_KEY, USER_TOKEN };
