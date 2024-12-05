"use client";
import { createContext, useContext, useState } from "react";

// Create a context
const RawDataContext = createContext();

export const RawDataProvider = ({ children }) => {
  const [rawData, setRawData] = useState({ file: {}, csvData: [] });
  return (
    <RawDataContext.Provider value={{ rawData, setRawData }}>
      {children}
    </RawDataContext.Provider>
  );
};

export const useRawData = () => useContext(RawDataContext);
