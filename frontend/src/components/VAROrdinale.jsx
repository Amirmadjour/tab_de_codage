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

const FormSchema = z.object({
  colonnes: z.array(z.string()).refine((value) => value.some((item) => item), {
    message: "You have to select at least one item.",
  }),
});

export default function VAROrdinale({
  colonnes,
  setVariablesOrdinales,
  setData,
  data,
}) {
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
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
        <FormField
          control={form.control}
          name="colonnes"
          render={() => (
            <FormItem>
              <div className="mb-4">
                <FormLabel className="text-base">Variable ordinales</FormLabel>
                <FormDescription>
                  Veuiller choisir les variables ordinales
                </FormDescription>
              </div>
              {colonnes.map((colonne) => (
                <FormField
                  key={colonne}
                  control={form.control}
                  name="colonnes"
                  render={({ field }) => {
                    return (
                      <FormItem
                        key={colonne}
                        className="flex flex-row items-start space-x-3 space-y-0"
                      >
                        <FormControl>
                          <Checkbox
                            checked={field.value?.includes(colonne)}
                            onCheckedChange={(checked) => {
                              return checked
                                ? field.onChange([...field.value, colonne])
                                : field.onChange(
                                    field.value?.filter(
                                      (value) => value !== colonne
                                    )
                                  );
                            }}
                          />
                        </FormControl>
                        <FormLabel className="text-sm font-normal">
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
