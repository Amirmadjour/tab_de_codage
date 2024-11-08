"use client";
import { useRawData } from "@/components/RawDataContext";
import React from "react";

const page = () => {
  const { rawData } = useRawData();
  return (
    <table>
      <thead>
        <tr>
          {rawData.csvData.length > 0 &&
            Object.keys(rawData.csvData[0]).map((key) => (
              <th key={key}>{key}</th>
            ))}
        </tr>
      </thead>
      <tbody>
        {rawData.csvData.map((row, index) => (
          <tr key={index}>
            {Object.values(row).map((value, i) => (
              <td key={i}>{value}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default page;
