"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import CustomField from "./CustomField";
import { useEffect } from "react";
import axios from "@/lib/axios";
import { useMutation } from "@tanstack/react-query";

const formSchema = z.object({
  trainingset: z.number().min(0).max(100),
  testingset: z.number().min(0).max(100),
  popsize: z.number().min(5),
  epoch: z.number(),
});

const sca = async (parametres) => {
  const response = await axios.post("/sca/", parametres);
  return response.data;
};

export function CustomForm({ method }) {
  const mutation = useMutation({
    mutationFn: sca,
    mutationKey: ["sca"],
    onSuccess: (data) => {
      console.log("Post successful!", data);
    },
    onError: (error) => {
      console.error("Error posting data:", error);
    },
  });

  const formItems = [
    [
      { key: "trainingset", label: "Training Set" },
      { key: "testingset", label: "Testing Set" },
    ],
    [
      { key: "popsize", label: "Population size" },
      { key: "epoch", label: "Epoch" },
    ],
  ];
  const form = useForm({
    resolver: zodResolver(formSchema),
    defaultValues: {
      trainingset: 70,
      testingset: 30,
      popsize: 5,
      epoch: 10,
    },
  });

  // Watch testingset value and update trainingset dynamically
  const { watch, setValue } = form;
  const testingset = watch("testingset");
  const trainingset = watch("trainingset");
  const popsize = watch("popsize");
  const epoch = watch("epoch");

  useEffect(() => {
    if (testingset !== undefined && testingset.toString().length != 0) {
      setValue("trainingset", parseInt(100 - testingset));
      setValue("testingset", parseInt(testingset));
    }
  }, [testingset, setValue]);

  useEffect(() => {
    if (trainingset !== undefined && trainingset.toString().length != 0) {
      setValue("testingset", parseInt(100 - trainingset));
      setValue("trainingset", parseInt(trainingset));
    }
  }, [trainingset, setValue]);

  useEffect(() => {
    if (popsize !== undefined && popsize.toString().length != 0) {
      setValue("popsize", parseInt(popsize));
    }
  }, [popsize, setValue]);

  useEffect(() => {
    if (epoch !== undefined && epoch.toString().length != 0) {
      setValue("epoch", parseInt(epoch));
    }
  }, [epoch, setValue]);

  function onSubmit(values) {
    console.log(values);
    values = {
      ...values,
      trainingset: trainingset / 100,
      testingset: testingset / 100,
      method: method,
    };
    mutation.mutate(values);
  }

  return (
    <Form {...form}>
      <form
        onSubmit={form.handleSubmit(onSubmit)}
        className="w-full h-full flex flex-col items-center justify-between"
      >
        {/* Dynamically create form fields based on defaultValues */}
        <div className="flex flex-col items-center justify-center gap-2.5">
          <FormLabel className="text-left w-full text-xl font-medium text-[#000] opacity-100">
            Dataset split
          </FormLabel>
          <div className="w-full h-fit flex items-center justify-center gap-2.5">
            {formItems[0].map((i) => (
              <CustomField key={i.key} form={form} item={i} />
            ))}
          </div>
          <FormLabel className="text-left w-full text-xl font-medium text-[#000] opacity-100">
            Algorithm properties
          </FormLabel>
          <div className="w-full h-fit flex flex-col items-center justify-center gap-2.5">
            {formItems[1].map((i) => (
              <CustomField key={i.key} form={form} item={i} />
            ))}
          </div>
        </div>
        <div className="w-full h-fit flex items-center justify-center gap-2.5">
          <Button
            type="submit"
            className="w-full text-white rounded-lg bg-accent py-2 "
            disabled={mutation.isPending}
          >
            Run Algorithm
          </Button>
          <Button
            disabled
            className="w-full text-white rounded-lg bg-primary py-2 "
          >
            Download CSV file
          </Button>
        </div>
      </form>
    </Form>
  );
}
