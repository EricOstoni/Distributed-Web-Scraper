// import http from "k6/http";
// import { check, sleep } from "k6";

// export let options = {
//   stages: [
//     { duration: "30s", target: 100 },
//     { duration: "1m", target: 500 },
//     { duration: "1m", target: 1000 },
//     { duration: "30s", target: 0 },
//   ],
// };

// export default function () {
//   const res = http.get("http://34.102.218.251/api/products");
//   // const res = http.get("https://www.google.com/");

//   check(res, {
//     "status is 200": (r) => r.status === 200,
//     "response time < 500ms": (r) => r.timings.duration < 500,
//   });

//   sleep(1);
// }

import http from "k6/http";
import { check, sleep } from "k6";

export let options = {
  stages: [
    { duration: "30s", target: 250 }, // postupno do 250
    { duration: "30s", target: 500 }, // povećaj do 500
    { duration: "30s", target: 1000 }, // puni load
    { duration: "1m", target: 1000 }, // zadrži 1 min
    { duration: "30s", target: 0 }, // smanji na 0
  ],
  thresholds: {
    http_req_duration: ["p(95)<3000"], // 95% requestova ispod 3s
    http_req_failed: ["rate<0.01"], // manje od 1% failanih zahtjeva
  },
};

const keywords = ["iphone", "macbook", "ipad", "watch", "mac"];
const categoryMap = {
  iphone: "iphone",
  macbook: "macbook",
  ipad: "ipad",
  watch: "watch",
  mac: "mac",
};

export default function () {
  const keyword = keywords[Math.floor(Math.random() * keywords.length)];

  const scraperRes = http.post(
    `http://34.102.218.251/api/scraper?keyword=${keyword}`
  );
  check(scraperRes, {
    "POST /scraper status 200": (res) => res.status === 200,
  });

  const jobId = scraperRes.json("job_id");
  if (!jobId) return;

  let jobDone = false;
  for (let i = 0; i < 5; i++) {
    const statusRes = http.get(
      `http://34.102.218.251/api/job-status?job_id=${jobId}`
    );
    const status = statusRes.json("status");

    if (status === "finished") {
      jobDone = true;
      break;
    }
    sleep(2);
  }

  if (jobDone) {
    const category = categoryMap[keyword];
    const productRes = http.get(
      `http://34.102.218.251/api/products?category=${category}`
    );
    check(productRes, {
      "GET /products status 200": (res) => res.status === 200,
      "GET /products not empty": (res) => res.json().length > 0,
      "GET /products < 2s": (res) => res.timings.duration < 2000,
    });
  }
}
