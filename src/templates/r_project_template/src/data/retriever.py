from loguru import logger
from pathlib import Path
import httpx
import pandas as pd 
import os

'''Implement this function to retrieve data from a url resource'''
def retriever():
    

    # Change these
    url = "https://official-joke-api.appspot.com/random_joke"
    timeout = 10
    headers = None 
    params = None

    logger.info("Trying to retrieve raw data")
    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.get(url, params=params, headers=headers)
            response.raise_for_status()  # Raise if not 2xx

            content_type = response.headers.get("content-type", "").lower()

            # -----------------------------
            # Determine return type
            # -----------------------------
            if "application/json" in content_type:
                data = response.json()
            elif "text/" in content_type:
                data = response.text
            else:
                data = response.content  # raw bytes

        if isinstance(data, dict):
            df = pd.DataFrame([data])  # Wrap dict in a list to create a single-row DataFrame
        elif isinstance(data, list):
            # If the API returns a list of dictionaries directly
            df = pd.DataFrame(data)
        else:
            # Handle text or other formats
            df = pd.DataFrame({"content": [data]})

        # Write raw data to raw/ 
        df.to_csv(_format_file2write())

    except httpx.HTTPStatusError as exc:
        raise RuntimeError(
            f"Request failed with HTTP {exc.response.status_code}: {exc.request.url}"
        ) from exc

    except httpx.RequestError as exc:
        raise RuntimeError(
            f"Network error while requesting {exc.request.url}: {exc}"
        ) from exc



def _format_file2write() -> str:
    script_dir = Path(__file__).parent
    target_dir = script_dir / "."
    raw_dir = "/raw/"

    existing_files = sorted(os.listdir(target_dir.__str__() + raw_dir))

    if len(existing_files) == 0:
        return target_dir.__str__() + raw_dir + "raw_data_1.csv"
    else:
        last_file = existing_files[-1]
        num_last_file = int(last_file[9:-4])
        num_new_file = num_last_file + 1
        new_file = target_dir.__str__() + raw_dir + "raw_data_" + str(num_new_file) + ".csv"
        logger.info(f"Writing raw data to {"raw_data_" + str(num_new_file) + ".csv"}.")
        return new_file
    





if __name__=="__main__":
    retriever()
