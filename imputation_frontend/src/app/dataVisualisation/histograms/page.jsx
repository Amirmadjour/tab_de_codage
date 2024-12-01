"use client";
import React from "react";
import { useQuery } from "@tanstack/react-query";
import axios from "@/lib/axios";

const page = () => {
  const gethistograms = async () => {
    const { data } = await axios.get("/histogram/");
    console.log(data);
    return JSON.parse(data);
  };

  const histograms = useQuery({
    queryKey: ["histograms"],
    queryFn: () => gethistograms(),
  });

  if (histograms.isLoading) return <div>Loading...</div>;
  if (histograms.isError)
    return <div className="text-red-400">{histograms.error.message}</div>;

  return <>Gottem</>;
};

export default page;
