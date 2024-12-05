"use client";
import axios from "@/lib/axios";
import { useQuery } from "@tanstack/react-query";
import { MyChart } from "./boxplot";

const page = () => {
  const getboxplot = async () => {
    const { data } = await axios.get("/boxplot/");
    return data;
  };

  const boxplot = useQuery({
    queryKey: ["boxplot"],
    queryFn: () => getboxplot(),
  });

  if (boxplot.isLoading)
    return <div className="text-blue-400">Loading....</div>;
  if (boxplot.isError)
    return <div className="text-red-500">{boxplot.error.message}</div>;

  console.log(boxplot.data);
  return (
    <div className="w-full h-full grid grid-cols-2 gap-3">
      {boxplot.data.map(
        (i) => i.key && i.value && <MyChart key={i.key} boxplot_data={i} />
      )}
    </div>
  );
};

export default page;
