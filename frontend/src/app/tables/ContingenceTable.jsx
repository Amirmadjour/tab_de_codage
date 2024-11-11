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
  const fi = content.Ni;
  const fj = content.Nj;

  console.log("fi: ", fi);
  console.log("fj: ", fj);

  return (
    <div className="w-full">
      <h3></h3>
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
      <div className="[&_span]:text-muted-foreground flex flex-col gap-2 border p-5 overflow-auto rounded-[10px]">
        <p className="">
          <span>Centre de gravité:</span> {content.centre_de_gravite[0]}
          {", "}
          {content.centre_de_gravite[1]}
        </p>
        <div>
          <p>
            <span>F(I):</span>
            {`{${fi.map((i) => `[(${i[0].join("; ")}); ${i[1]}]`).join(", ")}}`}
          </p>
        </div>
        <div>
          <p>
            <span>F(J):</span>
            {`{${fj.map((i) => `[(${i[0].join("; ")}); ${i[1]}]`).join(", ")}}`}
          </p>
        </div>
      </div>
    </div>
  );
};

export default ContingenceTable;
