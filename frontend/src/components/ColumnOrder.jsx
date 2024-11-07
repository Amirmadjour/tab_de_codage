"use client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { useForm } from "react-hook-form";
import { toast } from "@/hooks/use-toast";
import { useData } from "./DataContext";

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
    <form onSubmit={handleSubmit(onSubmit)}>
      {variablesAOrder.map((v, index) => (
        <div
          key={index}
          className="select-none cursor-grab hover:font-bold hover:bg-gray-300"
          draggable
          onDragStart={(e) => handleOnDrag(e, v)}
        >
          {v}
        </div>
      ))}
      <div
        className="w-full h-fit min-h-20 bg-blue-400"
        onDrop={(e) => {
          handleOnDrop(e);
        }}
        onDragOver={handleDragOver}
      >
        {order.map((o, index) => (
          <div key={index}>{o}</div>
        ))}
      </div>
      <div className="flex gap-2">
        <Button
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
