"use client";
import { useRawData } from "@/components/RawDataContext";
import React from "react";

const page = () => {
  const { rawData } = useRawData();

  console.log("file: ", rawData.file);

  return <div>{rawData.file.name}</div>;
};

export default page;
