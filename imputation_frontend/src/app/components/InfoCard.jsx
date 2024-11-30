import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { FileX2 } from "lucide-react";

const InfoCard = ({ title, time, description }) => {
  return (
    <Card className="shrink-0 relative overflow-hidden rounded-[12px] border-none p-4 flex flex-col items-start justify-center gap-2.5 h-fit w-[410px]">
      <div className="absolute left-0 h-full w-1 bg-blue-600"></div>
      <CardHeader className="flex flex-row items-center justify-center gap-2.5 p-0">
        <div className="flex items-center justify-center bg-[#0000001A] h-fit w-fit p-2 rounded-full">
          <FileX2 />
        </div>
        <CardTitle className="text-[18px] !m-0">{title}</CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col items-start justify-center gap-0.5 p-0">
        <p className="text-[#00000066] text-[14px]">{time}</p>
        <p className="text-lg leading-[24px]">{description}</p>
      </CardContent>
    </Card>
  );
};

export default InfoCard;
