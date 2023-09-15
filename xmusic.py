import requests
from json import JSONDecodeError
import os

RED = "\033[91m"
END = "\033[0m"
BLUE = "\033[94m"
GREEN = "\033[92m"


# Definitions
def slugify(value: str):
    forbidden = "/><:\"\\|?*"
    for each in forbidden: value: str = value.replace(each, " ")

    value: str = value.title()
    value: str = value.replace("  ", "")

    return f"{value}"


def ok(query_response: dict, quality_param: str):
    if "vid" not in query_response \
            or "token" not in query_response \
            or "timeExpires" not in query_response \
            or "links" not in query_response \
            or "title" not in query_response:

        return False

    _links: dict = query_response.get("links", None)
    _mp3: dict = _links.get("mp3", None)
    if _mp3 is None: return False
    _quality: dict = _mp3.get(quality_param, None)
    return "k" in _quality


# Headers
query_headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-requested-with": "XMLHttpRequest",
    "Referer": "https://x2download.app/en105/download-youtube-to-mp3",
    "Referrer-Policy": "strict-origin-when-cross-origin"
}

convert_headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
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
}

os.system("cls")
download_directory: str = input("Directory: ")
print("\n")

downloaded_count = 0

while True:
    context: str = f"[{downloaded_count}]"
    url: str = input(f"{BLUE}{context} Identifier{END}: ")
    quality = "4"
    ft: str = "mp3"

    # Initiate Query Request
    query: requests.Response = requests.post("https://x2download.app/api/ajaxSearch", headers=query_headers,
                                             data={
                                                 "q": url,
                                                 "vt": ft
                                             })
    
    # Validate Query Response
    try:
        json_res: dict = query.json()
        if not ok(json_res, quality):
            print(f"{RED}[0] Failed: Please check your internet connection.{END}")
            continue

        # Initiate Conversion Request
        conversion: requests.Response = requests.post("https://backend.svcenter.xyz/api/convert-by-45fc4be8916916ba3b8d61dd6e0d6994", headers=convert_headers,
                                                      data={
                                                          'v_id': json_res['vid'],
                                                          'ftype': ft,
                                                          'fquality': json_res['links']['mp3'][quality]['k'],
                                                          'token': json_res['token'],
                                                          'timeExpire': json_res['timeExpires'],
                                                          'client': 'X2Download.app',
                                                      })
        
        # Validate Conversion Status
        con_json: dict = conversion.json()

        # Failure
        if con_json.get("c_status", "fail") != "ok" or con_json.get("d_url", "") == "":
            print(f"{RED}[1] Failed: Please check your internet connection.{END}")
            continue

        # Pre Generate Filename
        filename = slugify(json_res["title"])
        extra_n = 0
        final_filename: str = f"{filename}.{ft}"

        # Generate Filename
        while True:
            if not os.path.exists(f"{download_directory}/{final_filename}"): break
            extra_n += 1
            if extra_n != 0: final_filename = f"{filename} [{extra_n}].{ft}"

        # Directory Creation
        if not os.path.exists(download_directory) or not os.path.isdir(download_directory): os.mkdir(download_directory)

        # Output Response
        download_response = requests.get(con_json.get("d_url"), stream=True)
        print(con_json.get("d_url"))

        # Output Stream
        with open(f"{download_directory}/{final_filename}", "wb") as file:
            for chunk in download_response.iter_content(chunk_size=1024):
                if chunk: file.write(chunk)

        # Increment Downloaded Count
        if extra_n != 0: print(f"{GREEN}Downloaded{END}: \"{filename} [{extra_n}]\"\n")
        else: print(f"{GREEN}Downloaded{END}: \"{filename}\"\n")
        downloaded_count += 1

    except JSONDecodeError:
        print(f"{RED}[2] Failed: Please check your internet connection.{END}")
        continue
