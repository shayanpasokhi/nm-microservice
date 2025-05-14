import DefaultLayout from "../layouts/Default";
import NotFound from "../pages/not-found";
import LoginRegister from "../pages/login-register";
import FilePage from "../pages/FilePage";
import LoginIcon from "@mui/icons-material/Login";
import InsertDriveFileIcon from "@mui/icons-material/InsertDriveFile";
import FindInPageIcon from "@mui/icons-material/FindInPage";
import ScanPage from "../pages/ScanPage";

const indexRoutes = [
  {
    path: "/",
    component: DefaultLayout,
    routes: [
      {
        path: "/login-register",
        name: "ورود / ثبت‌نام",
        component: LoginRegister,
        private: false,
        showInStepper: true,
        icon: <LoginIcon />,
      },
      {
        path: "/file",
        name: "انتخاب فایل",
        component: FilePage,
        private: true,
        showInStepper: true,
        icon: <InsertDriveFileIcon />,
      },
      {
        path: "/scan",
        name: "پویش",
        component: ScanPage,
        private: true,
        showInStepper: true,
        icon: <FindInPageIcon />,
      },
      {
        path: "/",
        pathTo: "/file",
        redirect: true,
      },
    ],
  },
  { path: "*", component: NotFound },
];

export default indexRoutes;
