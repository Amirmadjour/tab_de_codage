import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs) {
  return twMerge(clsx(inputs));
}

//Turns an object of objects into an array of objects
export function conTabs(tabContingence) {
  let arr = [];
  for (let key in tabContingence) {
    arr = [...arr, tabContingence[key]];
  }
  return arr;
}

//Expected input: arr:[] of {tableau: {columns: [], index: [], data: []}, ...}
//Exprected output: arr:[] of objects {group, variable, value}

export function formDataToHeatMap(data) {
  let arr = [];

  const vars = data.columns;
  const groups = data.index;
  const values = data.data;

  for (let i = 0; i < vars.length; i++) {
    for (let j = 0; j < groups.length; j++) {
      const obj = {
        group: groups[j],
        variable: vars[i],
        value: values[j][i],
      };
      arr = [...arr, obj];
    }
  }

  return arr;
}
