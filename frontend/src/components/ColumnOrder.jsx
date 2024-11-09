"use client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { useForm } from "react-hook-form";
import { toast } from "@/hooks/use-toast";
import { useData } from "./DataContext";
import DragHandleSVG from "@/assets/svg/DragHandleSVG";

const ColumnOrder = ({ variables, reponses, currentRep }) => {
  const { register, handleSubmit, setValue, reset } = useForm();
  const [order, setOrder] = useState([]);
  const { data, setData } = useData();
  const [variablesAOrder, setVariablesAOrder] = useState(variables);

  setValue("order", order);

  function handleOnDrag(e, orderType) {
    e.dataTransfer.setData("orderType", orderType);
  }

  function handleOnDrop(e) {
    const orderType = e.dataTransfer.getData("orderType");
    const updatedOrder = [...order, orderType];
    setOrder(updatedOrder);
    setValue("order", updatedOrder);
    setVariablesAOrder(variablesAOrder.filter((i) => i !== orderType));
  }

  function handleDragOver(e) {
    e.preventDefault();
  }

  useEffect(() => {
    setVariablesAOrder(variables);
    setOrder([]);
  }, [variables]);

  function onSubmit(SubmittedData) {
    const newData = { ...data };
    newData[currentRep] = SubmittedData.order;
    console.log(newData);
    setData(newData);
    toast({
      title: "You submitted the following values:",
      description: (
        <pre className="mt-2 w-[340px] rounded-md bg-slate-950 p-4">
          <code className="text-white">{JSON.stringify(newData, null, 2)}</code>
        </pre>
      ),
    });
  }

  return (
    <form
      onSubmit={handleSubmit(onSubmit)}
      className="flex flex-col items-start justify-start gap-2.5 w-full"
    >
      <h2 className="text-lg">Select ordinal variables</h2>
      {variablesAOrder.map((v, index) => (
        <div
          key={index}
          className="w-full flex items-center justify-start gap-2.5 select-none cursor-grab hover:bg-hover h-10 rounded-[10px]"
          draggable
          onDragStart={(e) => handleOnDrag(e, v)}
        >
          <DragHandleSVG />
          {v}
        </div>
      ))}
      <div
        className="dashed-drag-n-drop w-full h-fit min-h-20 p-2.5 numbered-list"
        onDrop={(e) => {
          handleOnDrop(e);
        }}
        onDragOver={handleDragOver}
      >
        {order.map((o, index) => (
          <div
            key={index}
            className="w-full flex items-center justify-start select-none hover:bg-hover h-10 rounded-[10px] px-2"
          >
            {o}
          </div>
        ))}
      </div>

      <div className="flex gap-2">
        <Button
          className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
          onClick={(e) => {
            e.preventDefault();
            setOrder([]);
            setVariablesAOrder(variables);
          }}
        >
          Réinitialiser
        </Button>
        <input
          type="hidden"
          {...register("order")}
          value={JSON.stringify(order)}
        />
        <Button type="submit">Submit Order</Button>
      </div>
    </form>
  );
};

export default ColumnOrder;
