import React, {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useState,
  useEffect,
} from "react";

const ReportContext = createContext(undefined);

const ReportProvider = ({ children }) => {
  const [report, setReport] = useState({});

  const cleanReport = () => {
    setReport({});
  };

  const addReport = (report) => {
    setReport((pre) => ({
      ...pre,
      ...report,
    }));
  };

  const value = useMemo(
    () => ({ report, addReport, cleanReport }),
    [report, addReport, cleanReport]
  );

  return (
    <ReportContext.Provider value={value}>{children}</ReportContext.Provider>
  );
};

const useReport = () => {
  const context = useContext(ReportContext);

  if (context === undefined)
    throw new Error("useAuth must be within ReportProvider!");

  return context;
};

export { ReportProvider, useReport };
