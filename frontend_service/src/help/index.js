import { toast } from "react-toastify";

export const errorToast = (msg) =>
  toast.error(msg || "خطا", {
    position: "bottom-right",
    autoClose: 5000,
    hideProgressBar: false,
    closeOnClick: true,
    pauseOnHover: true,
    draggable: true,
    progress: undefined,
  });

export const successToast = (msg) =>
  toast.success(msg || "عملیات با موفقیت انجام شد", {
    position: "bottom-right",
    autoClose: 5000,
    hideProgressBar: false,
    closeOnClick: true,
    pauseOnHover: true,
    draggable: true,
    progress: undefined,
  });

export const warnToast = (msg) =>
  toast.warn(msg || "هشدار", {
    position: "bottom-right",
    autoClose: 5000,
    hideProgressBar: false,
    closeOnClick: true,
    pauseOnHover: true,
    draggable: true,
    progress: undefined,
  });

export const getParentPath = (path) => {
  const segments = path.split("/");
  segments.pop();
  return segments.join("/");
};

export const getSize = (size) => {
  let sizes = [
    " Bytes",
    " KB",
    " MB",
    " GB",
    " TB",
    " PB",
    " EB",
    " ZB",
    " YB",
  ];

  for (let i = 1; i < sizes.length; i++) {
    if (size < Math.pow(1024, i))
      return (
        Math.round((size / Math.pow(1024, i - 1)) * 100) / 100 + sizes[i - 1]
      );
  }
  return size;
};

export const requiredValidation = {
  required: "لطفا این فیلد را تکمیل کنید!",
};

export const extractErrorMessage = (err) => {
  const data = err?.response?.data?.msg;

  if (typeof data === "string") {
    return data;
  }

  if (typeof data === "object" && data !== null) {
    return Object.values(data).flat().join(" - ");
  }

  return "خطا در درخواست";
};
