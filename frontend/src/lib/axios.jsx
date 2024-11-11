import axios from "axios";

const baseURL = process.env.NEXT_PUBLIC_URL;

console.log("Axios baseURL:", baseURL);
console.log("Environment variables:", process.env);


export default axios.create({
  baseURL: baseURL,
});
