"use client";
import { useRawData } from "@/components/RawDataContext";
import InfoSVG from "@/assets/svg/InfoSVG";
import React from "react";
import "./TableStyles.css";

const Page = () => {
  const { rawData } = useRawData();

  console.log("rawData: ", rawData);
  return (
    <div className="flex flex-col h-fit w-full">
      {Object.keys(rawData.file).length == 0 ? (
        <div className="bg-hover text-popover-foreground flex gap-2.5 items-center justify-start p-4 h-fit w-full rounded-[10px]">
          <InfoSVG />
          <p>Please upload a file to see it as a raw csv</p>{" "}
        </div>
      ) : (
        <table className="tableau_style">
          <thead>
            <tr>
              {Object.values(rawData.csvData[0]).map((value, i) => (
                <td key={i}>{value}</td>
              ))}
            </tr>
          </thead>
          <tbody>
            {rawData.csvData.slice(1).map((row, index) => (
              <tr key={index}>
                {Object.values(row).map((value, i) => (
                  <td key={i}>{value}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default Page;
