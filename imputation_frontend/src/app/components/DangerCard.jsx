import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { FileWarning, TriangleAlert } from "lucide-react";

const DangerCard = ({ title, time, description, icon }) => {
  return (
    <Card className="shrink-0 relative bg-accent overflow-hidden rounded-[12px] border-none p-4 flex items-center justify-between gap-2.5 h-fit w-[410px]">
      <div className="absolute left-0 h-full w-1 bg-accent"></div>
      <div className="flex flex-col items-start justify-center gap-2.5">
        <CardHeader className="flex flex-row items-center justify-center gap-2.5 p-0">
          <div className="flex items-center justify-center bg-[#FFFFFF1A] h-fit w-fit p-2 rounded-full">
            {icon}
          </div>
          <CardTitle className="text-[18px] !m-0 text-white">{title}</CardTitle>
        </CardHeader>
        <CardContent className="flex flex-col items-start justify-center gap-0.5 p-0">
          <p className="text-[#FFFFFF66] text-[14px]">{time}</p>
          <p className="text-lg leading-[24px] text-white">{description}</p>
        </CardContent>
      </div>
      <TriangleAlert className="text-white" />
    </Card>
  );
};

export default DangerCard;
