import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";

const CustomField = ({ form, item }) => {
  return (
    <FormField
      key={item.key}
      control={form.control}
      name={item.key}
      render={({ field }) => (
        <FormItem className="w-full h-fit">
          <FormLabel className="text-lg font-medium text-[#000] opacity-100">
            {item.label}
          </FormLabel>
          <FormControl>
            <Input placeholder={item.key} type="number" {...field} />
          </FormControl>
          <FormMessage />
        </FormItem>
      )}
    />
  );
};

export default CustomField;
