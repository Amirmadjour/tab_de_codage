import ResponsiveRectangle from "@/app/assets/SineCosineSVG";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { v4 as uuidv4 } from "uuid";
import Tab from "./components/Tab";

const page = () => {
  const nav = [
    { id: uuidv4(), val: "SCA" },
    { id: uuidv4(), val: "ESC" },
    { id: uuidv4(), val: "SHIO" },
  ];
  return (
    <div className="relative flex items-center justify-center w-full h-full">
      <ResponsiveRectangle />
      <Tabs
        defaultValue="SCA"
        className="flex flex-col items-center justify-center h-full w-full z-10"
      >
        <TabsList className="flex items-center justify-center gap-5 bg-transparent h-20 w-full">
          {nav.map((i) => (
            <TabsTrigger
              key={i.id}
              className="font-medium text-lg shadow-none px-8 py-3 rounded-full hover:bg-accent/10 data-[state=active]:bg-accent data-[state=active]:text-white"
              value={i.val}
            >
              {i.val}
            </TabsTrigger>
          ))}
        </TabsList>
        <Tab value="SCA" />
      </Tabs>
    </div>
  );
};

export default page;
