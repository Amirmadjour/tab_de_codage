import React, { useEffect, useState } from "react";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

const ContingenceTable = ({ content }) => {
  return (
    <div className="w-full">
      <Table className="">
        <TableHeader>
          <TableRow>
            <TableHead></TableHead>
            {content.tableau.columns.map((i, index) => (
              <TableHead key={index}>{i}</TableHead>
            ))}
          </TableRow>
        </TableHeader>
        <TableBody>
          {content.tableau.data.map((i, i_index) => (
            <TableRow key={i_index}>
              <TableCell className="text-muted-foreground">
                {content.tableau.index[i_index]}
              </TableCell>
              {i.map((j, j_index) => (
                <TableCell key={i_index.toString() + j_index.toString()}>
                  {j}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
};

export default ContingenceTable;
