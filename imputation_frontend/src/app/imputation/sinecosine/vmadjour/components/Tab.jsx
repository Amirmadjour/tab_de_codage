"use client";
import { TabsContent } from "@/components/ui/tabs";
import { CustomForm } from "./CustomForm";
import { Label } from "@/components/ui/label";
import LineChart from "./LineChart";
import MultipleLineChart from "./MultipleLineChart";
import { useState } from "react";

const Tab = ({ value }) => {
  const [data, setData] = useState({ Fit: {}, accuracies: {} });
  const [f1_scoreData, setF1_scoreData] = useState({});
  const socket = new WebSocket("ws://localhost:8000/ws/accuracy/");
  socket.onopen = function (event) {
    console.log("WebSocket is connected.");
  };

  socket.onmessage = (event) => {
    const dataWs = JSON.parse(event.data);
    const acc = dataWs.accuracy;
    const f1 = dataWs.f1_score;
    //console.log("acc:", acc);
    //console.log("f1_score:", f1);
    const fit = acc
      ? Object.fromEntries(
          Object.entries(acc).map(([key, value]) => [key, 1 - value])
        )
      : {};

    //console.log(fit);
    setData((prev) => {
      const prevFit = prev?.Fit || {};
      return {
        accuracies: { ...prev?.accuracies },
        Fit: {
          ...prevFit,
          ...fit,
        },
      };
    });
    setF1_scoreData((prev) => {
      const prevF1_scores = prev?.f1_scores || {};
      return {
        f1_scores: {
          ...prevF1_scores,
          ...f1,
        },
      };
    });
    setData((prev) => {
      const prevAccuracies = prev?.accuracies || {};
      return {
        Fit: { ...prev?.Fit },
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
      className="flex items-center justify-center w-full h-full p-0 m-0 gap-2.5 data-[state=inactive]:hidden"
    >
      <div className="shrink-0 w-[500px] h-full shadow-sm rounded-2xl bg-[#FFFFFF80] p-5">
        <CustomForm method={value} />
      </div>
      <div className="w-full h-full flex flex-col items-center justify-center gap-2.5 ">
        <div className="grow w-full shadow-sm rounded-2xl bg-[#ffffff80] p-2 flex flex-col items-center justify-center">
          <Label className="font-medium text-lg">
            Fitness and Accuracy Line chart
          </Label>
          <MultipleLineChart chartData={data} />
        </div>
        <div className="grow w-full shadow-sm rounded-2xl bg-[#FFFFFF80] p-2 flex flex-col items-center justify-center">
          <Label className="font-medium text-lg">F1-score Line chart</Label>
          <LineChart chartData={f1_scoreData.f1_scores} />
        </div>
      </div>
    </TabsContent>
  );
};

export default Tab;
