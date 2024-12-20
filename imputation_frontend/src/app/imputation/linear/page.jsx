"use client";
import { useQuery } from "@tanstack/react-query";
import axios from "@/lib/axios";
import SingleTable from "@/app/components/SingleTableBadache";
import { SkeletonTable } from "@/app/components/SkeletonComponent";


const page = () => {
  const getregression = async () => {
    const { data } = await axios.get("/multiple-linear-regression/");
    return JSON.parse(data);
  };

  const regression = useQuery({
    queryKey: ["regression"],
    queryFn: () => getregression(),
  });

  if (regression.isLoading)
    return (
      <div>
        <SkeletonTable />
      </div>
    );
  if (regression.isError)
    return <div className="text-red-400">{regression.error.message}</div>;

    return <SingleTable
      content={regression.data}
      className="border-collapse w-full"
  />;
};

export default page;