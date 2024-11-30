import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import clsx from "clsx";

const InfoCard = ({
  title,
  time,
  description,
  icon,
  strip_variant = "info",
}) => {
  const strip_variant_class = {
    info: "bg-secondary",
    success: "bg-[#76C263]",
    danger: "bg-accent",
  };
  return (
    <Card className="shrink-0 relative overflow-hidden rounded-[12px] border-none p-4 flex flex-col items-start justify-center gap-2.5 h-fit w-[410px]">
      <div
        className={clsx(
          "absolute left-0 h-full w-1 ",
          strip_variant_class[strip_variant]
        )}
      ></div>
      <CardHeader className="flex flex-row items-center justify-center gap-2.5 p-0">
        <div className="flex items-center justify-center bg-[#0000001A] h-fit w-fit p-2 rounded-full">
          {icon}
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
