import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs) {
  return twMerge(clsx(inputs));
}

export function conTabs(tabContingence) {
  let arr = [];
  for (let key in tabContingence) {
    arr = [...arr, tabContingence[key]];
  }
  return arr;
}
