"use client";
import { createContext, useContext, useState } from "react";

// Create a context
const DataContext = createContext();

export const DataProvider = ({ children }) => {
  const [data, setData] = useState({});
  return (
    <DataContext.Provider value={{ data, setData }}>
      {children}
    </DataContext.Provider>
  );
};

export const useData = () => useContext(DataContext);
