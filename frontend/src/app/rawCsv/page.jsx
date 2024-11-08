"use client";
import { useRawData } from "@/components/RawDataContext";
import React from "react";
import "./TableStyles.css";

const Page = () => {
  const { rawData } = useRawData();

  return (
    <table className="tableau_style">

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

export default Page;
