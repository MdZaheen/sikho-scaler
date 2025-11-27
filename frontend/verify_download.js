const http = require("http");

const url =
  "http://localhost:3000/api/download?url=https://www.w3schools.com/html/mov_bbb.mp4&filename=test.mp4";

http
  .get(url, (res) => {
    console.log("Status Code:", res.statusCode);
    console.log("Content-Disposition:", res.headers["content-disposition"]);
    console.log("Content-Type:", res.headers["content-type"]);
    res.resume(); // Consume response to free up memory
  })
  .on("error", (e) => {
    console.error(`Got error: ${e.message}`);
  });
