"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { useForm } from "react-hook-form";
import { toast } from "@/hooks/use-toast";

const ColumnOrder = ({ variables }) => {
  const { register, handleSubmit, setValue, reset } = useForm();
  const [order, setOrder] = useState([]);
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

  function onSubmit(data) {
    console.log(data);
    toast({
      title: "You submitted the following values:",
      description: (
        <pre className="mt-2 w-[340px] rounded-md bg-slate-950 p-4">
          <code className="text-white">{JSON.stringify(data, null, 2)}</code>
        </pre>
      ),
    });
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        {variablesAOrder.map((v) => (
          <div
            className="select-none cursor-grab"
            draggable
            onDragStart={(e) => handleOnDrag(e, v)}
          >
            {v}
          </div>
        ))}
        <div
          className="w-full h-fit min-h-20 bg-blue-400"
          onDrop={handleOnDrop}
          onDragOver={handleDragOver}
        >
          {order.map((o, index) => (
            <div key={index}>{o}</div>
          ))}
        </div>
        <Button
          onClick={(e) => {
            e.preventDefault();
            setOrder([]);
            setVariablesAOrder(variables);
          }}
        >
          Réinitialiser
        </Button>
        <button type="submit">Submit Order</button>
        <input
          type="hidden"
          {...register("order")}
          value={JSON.stringify(order)}
        />
      </div>
    </form>
  );
};

export default ColumnOrder;
