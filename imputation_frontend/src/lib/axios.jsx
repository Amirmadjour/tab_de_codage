import axios from "axios";

const baseURL = process.env.NEXT_PUBLIC_URL;

export default axios.create({
  baseURL: baseURL,
});
