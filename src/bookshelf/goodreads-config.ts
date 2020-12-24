// require("dotenv").config();

const goodreadsConfig: { [key: string]: string } = {
  key: process.env.VUE_APP_GOODREADS_KEY || "",
  id: process.env.VUE_APP_GOODREADS_ID || "",
};

export default goodreadsConfig;
