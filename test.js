fetch("https://backend.svcenter.xyz/api/convert-by-45fc4be8916916ba3b8d61dd6e0d6994", {
  "headers": {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "x-requested-key": "de0cfuirtgf67a",
    "Referer": "https://x2download.app/",
    "Referrer-Policy": "strict-origin-when-cross-origin"
  },
  "body": "v_id=-FP2Cmc7zj4&ftype=mp3&fquality=128&token=c4024492509a9c153020df6e2284553ce51bedc8e63eaeb7da8cb3d3c6000c27&timeExpire=1687760913&client=X2Download.app",
  "method": "POST"
}).then(res => res.json().then(json => console.log(json)));