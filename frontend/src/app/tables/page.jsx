"use client";
import { useRawData } from "@/components/RawDataContext";
import React from "react";
import InfoSVG from "@/assets/svg/InfoSVG";

const page = () => {
  const { rawData } = useRawData();

  return (
    <div className="flex flex-col h-fit w-full">
      {Object.keys(rawData.file).length == 0 && (
        <div className="bg-hover text-popover-foreground flex gap-2.5 items-center justify-start p-4 h-fit w-full rounded-[10px]">
          <InfoSVG />
          <p>Please upload a file to see results in tables</p>{" "}
        </div>
      )}
    </div>
  );
};

export default page;
