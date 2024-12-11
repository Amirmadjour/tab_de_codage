"use client";
import React from "react";
import { useQuery } from "@tanstack/react-query";
import axios from "@/lib/axios";
import SingleTable from "@/app/components/SingleTable";
import { SkeletonTable } from "@/app/components/SkeletonComponent";
import SingleTableBadache from "@/app/components/SingleTableBadache";

const page = () => {
  const getknn = async () => {
    const { data } = await axios.get("/knn/");
    return JSON.parse(data);
  };

  const knn = useQuery({
    queryKey: ["knn"],
    queryFn: () => getknn(),
  });

  if (knn.isLoading)
    return (
      <div>
        <SkeletonTable />
      </div>
    );
  if (knn.isError)
    return <div className="text-red-400">{knn.error.message}</div>;

  return <SingleTableBadache content={knn.data} />;
};

export default page;
