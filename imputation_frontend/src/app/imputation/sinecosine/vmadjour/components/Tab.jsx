"use client";
import { TabsContent } from "@/components/ui/tabs";
import { CustomForm } from "./CustomForm";
import { Label } from "@/components/ui/label";
import LineChart from "./LineChart";
import { useState } from "react";

const Tab = ({ value }) => {
  const [data, setData] = useState({});
  const socket = new WebSocket("ws://localhost:8000/ws/accuracy/");
  socket.onopen = function (event) {
    console.log("WebSocket is connected.");
  };

  socket.onmessage = (event) => {
    const dataWs = JSON.parse(event.data);
    const acc = dataWs.accuracy;
    console.log(acc);
    setData((prev) => {
      const prevAccuracies = prev?.accuracies || {}; 
      return {
        accuracies: {
          ...prevAccuracies, 
          ...acc, 
        },
      };
    });
  };

  return (
    <TabsContent
      value={value}
      className="flex items-center justify-center w-full h-full p-5 gap-2.5"
    >
      <div className="shrink-0 w-[500px] h-full shadow-sm rounded-2xl bg-[#FFFFFF80] p-5">
        <CustomForm setData={setData} />
      </div>
      <div className="w-full h-full flex flex-col items-center justify-center gap-2.5 ">
        <div className="grow w-full shadow-sm rounded-2xl bg-[#ffffff80] p-2 flex flex-col items-center justify-center">
          <Label className="font-medium text-lg">
            Fitness and Accuracy Line chart
          </Label>
          <LineChart chartData={data?.accuracies} />
        </div>
        <div className="grow w-full shadow-sm rounded-2xl bg-[#FFFFFF80] p-2 flex flex-col items-center justify-center">
          <Label className="font-medium text-lg">F1-score Line chart</Label>
          <LineChart chartData={data?.accuracies} />
        </div>
      </div>
    </TabsContent>
  );
};

export default Tab;
