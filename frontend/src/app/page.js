"use client";
import React, { useEffect, useState } from "react";
import DropZone from "@/components/DropZone";
import { useData } from "@/components/DataContext";
import { useRawData } from "@/components/RawDataContext";

const App = () => {
  const { rawData, setRawData } = useRawData();
  const { data, setData } = useData();

  return (
    <div className="flex flex-col w-full h-full items-start justify-start gap-2.5 overflow-auto">
      <div className="flex flex-col items-start justify-start gap-0.5">
        <h1 className="text-3xl">File Management</h1>
        <p className="text-xs text-foreground-secondary">
          Upload your csv file and see results
        </p>
      </div>

      <DropZone />

      {/*rawData.file && (
        <Button
          onClick={async () => {
            setFileReady((val) => !val);
          }}
        >
          Traiter le fichier
        </Button>
      )*/}
    </div>
  );
};

export default App;
