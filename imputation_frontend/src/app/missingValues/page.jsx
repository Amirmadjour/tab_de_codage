"use client";
import axios from "@/lib/axios";
import { useQuery } from "@tanstack/react-query";
import VerticalBar from "@/app/components/VerticalBar";

const page = () => {
  const getMissingValues = async () => {
    const { data } = await axios.get("/nbValManquantes/");
    return data;
  };

  const missingValues = useQuery({
    queryKey: ["missingData"],
    queryFn: () => getMissingValues(),
  });

  if (missingValues.isLoading)
    return <div className="text-blue-400">Loading....</div>;
  if (missingValues.isError)
    return <div className="text-red-500">{missingValues.error.message}</div>;

  return (
    <div className="w-full h-full">
      <VerticalBar graphicData={missingValues.data} />
    </div>
  );
};

export default page;
