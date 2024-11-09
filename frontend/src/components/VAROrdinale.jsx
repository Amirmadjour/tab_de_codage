"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { toast } from "@/hooks/use-toast";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { useData } from "@/components/DataContext";
import { useState } from "react";
import clsx from "clsx";

const FormSchema = z.object({
  colonnes: z.array(z.string()),
});

export default function VAROrdinale({ colonnes, setVariablesOrdinales }) {
  const { data, setData } = useData();
  const form = useForm({
    resolver: zodResolver(FormSchema),
    defaultValues: {
      colonnes: [],
    },
  });

  function onSubmit(submittedData) {
    setVariablesOrdinales(submittedData);
    const newData = {};
    submittedData.colonnes.forEach((field) => {
      newData[field] = [];
    });
    setData({ ordinal_cols: newData });
    toast({
      title: "You submitted the following values:",
      description: (
        <pre className="mt-2 w-[340px] rounded-md bg-slate-950 p-4">
          <code className="text-white">
            {JSON.stringify({ ordinal_cols: newData }, null, 2)}
          </code>
        </pre>
      ),
    });
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8 w-full">
        <FormField
          control={form.control}
          name="colonnes"
          render={() => (
            <FormItem>
              <div className="mb-4">
                <FormLabel className="text-lg">
                  Select ordinal variables
                </FormLabel>
              </div>
              {colonnes.map((colonne) => (
                <FormField
                  key={colonne}
                  control={form.control}
                  name="colonnes"
                  render={({ field }) => {
                    const isChecked = field.value?.includes(colonne);
                    return (
                      <FormItem
                        key={colonne}
                        onMouseDown={(e) => {
                          e.preventDefault();
                          const checked = !isChecked;
                          if (checked) {
                            field.onChange([...field.value, colonne]);
                          } else {
                            field.onChange(
                              field.value.filter((value) => value !== colonne)
                            );
                          }
                        }}
                        className={clsx(
                          "flex flex-row items-center justify-start space-x-5 space-y-0 px-4 hover:bg-hover h-10 rounded-[10px] border border-transparent",
                          field.value?.includes(colonne) &&
                            "border border-primary"
                        )}
                      >
                        <FormControl>
                          <Checkbox
                            className="ring-0 shadow-none"
                            checked={field.value?.includes(colonne)}
                          />
                        </FormControl>
                        <FormLabel className="text-lg font-normal">
                          {colonne}
                        </FormLabel>
                      </FormItem>
                    );
                  }}
                />
              ))}
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">Submit</Button>
      </form>
    </Form>
  );
}
