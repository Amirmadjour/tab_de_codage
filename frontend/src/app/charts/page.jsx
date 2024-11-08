"use client";
import React from "react";
import InfoSVG from "@/assets/svg/InfoSVG";
import { useRawData } from "@/components/RawDataContext";

const page = () => {
  const { rawData } = useRawData();
  return (
    <div className="flex flex-col h-fit w-full">
      {Object.keys(rawData.file).length == 0 && (
        <div className="bg-hover text-popover-foreground flex gap-2.5 items-center justify-start p-4 h-fit w-full rounded-[10px]">
          <InfoSVG />
          <p>Please upload a file to see results in charts</p>{" "}
        </div>
      )}
    </div>
  );
};

export default page;
