import React from "react";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

const SingleTable = ({ title, content }) => {
  return (
    <div className="w-full flex flex-col items-center justify-center gap-5">
      {content.data.length != 0 && (
        <>
          <h2 className="text-3xl font-bold text-left w-full">{title}</h2>
          <Table className="">
            <TableHeader>
              <TableRow>
                {content.columns.map((i, index) => (
                  <TableHead key={index}>V{i}</TableHead>
                ))}
              </TableRow>
            </TableHeader>
            <TableBody>
              {content.data.map((i, i_index) => (
                <TableRow key={i_index}>
                  {i.map((j, j_index) => (
                    <TableCell key={i_index.toString() + j_index.toString()}>
                      {j}
                    </TableCell>
                  ))}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </>
      )}
    </div>
  );
};

export default SingleTable;
