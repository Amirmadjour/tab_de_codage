"use client";
import { useQuery } from "@tanstack/react-query";
import axios from "@/lib/axios";
import SingleTableBadache from "@/app/components/SingleTableBadache";
import { SkeletonTable } from "@/app/components/SkeletonComponent";


const page = () => {
  const getregression = async () => {
    const { data } = await axios.get("/polynomial/");
    return JSON.parse(data);
  };

  const polynomial = useQuery({
    queryKey: ["polynomial"],
    queryFn: () => getregression(),
  });

  if (polynomial.isLoading)
    return (
      <div>
        <SkeletonTable />
      </div>
    );
  if (polynomial.isError)
    return <div className="text-red-400">{polynomial.error.message}</div>;

  return <SingleTableBadache content={polynomial.data} />;
};

export default page;
