import csv
import requests
from pydantic import ValidationError
from infotrie.schema import CompanyDataModel
from google.cloud import storage
from dotenv import load_dotenv
import os
from pathlib import Path
import json
from typing import List
from tqdm import tqdm

def stream_csv_from_gcs(bucket_name: str, file_name: str, batch_size: int):
    storage_client = storage.Client.from_service_account_json(CREDENTIALS_PATH, project=os.environ.get("PROJECT_ID"))
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    content = blob.download_as_text()
    reader = csv.DictReader(content.splitlines(), delimiter=",")
    batch = []
    for row in reader:
        if row.get("company"):
            batch.append(row.get("company"))
            if len(batch) == batch_size:
                yield batch
                batch = []
        else:
            print(row)
            break
    if batch:
        yield batch

def fetch_data(api_url: str, header: dict, params: dict) -> List[dict]:
    response = requests.get(api_url, headers=header, params=params)
    response.raise_for_status()
    return response.json().get("Result")

def validate_data(data: dict) -> CompanyDataModel:
    print(data)
    try:
        validated_data = CompanyDataModel(**data)
        print("Validation Successful")
        return validated_data
    except ValidationError as e:
        print(f"Validation Error: {e.json(indent=4)}")
        raise

def transform_for_bigquery(data: CompanyDataModel) -> dict:
    transformed_data = data.dict()
    transformed_data["listings"] = [
        {"Code": listing.Code, "Exchange": listing.Exchange, "Name": listing.Name} for listing in transformed_data["listings"].values()
    ]
    transformed_data["officers"] = [
        {"Name": officer.name, "Title": officer.Title, "YearBorn": officer.YearBorn} for officer in transformed_data["officers"].value()
    ]
    return transformed_data

def main() -> None:
    api_url = "https://feed.finsents.com/idata/company_profile"
    bucket_name = os.environ.get("BUCKET_NAME")
    file_name = os.environ.get("FILE_NAME")

    params_list = stream_csv_from_gcs(bucket_name, file_name, batch_size=100)

    all_transformed_data = []

    for param in tqdm(params_list):
        for row in param:
            raw_data = fetch_data(api_url, header=HEADER, params={"symbol_name": row.strip()})
            for company in raw_data:
                print(company)
                validated_data = validate_data(company)
                transformed_data = transform_for_bigquery(validated_data)
                all_transformed_data.append(transformed_data)
                if len(all_transformed_data) == 10:
                    break

    with open("transformed_data.json", "w") as f:
        json.dump(all_transformed_data, f)

if __name__ == "__main__":
    BASE_DIR = Path(__file__).absolute().parent.parent

    load_dotenv(BASE_DIR / ".env")
    CREDENTIALS_PATH = str(BASE_DIR/"credentials"/"google_credentials.json")
    os.environ["GOOGLE_APPLICATION_CREDENITIALS"] = CREDENTIALS_PATH

    HEADER = {
        "Accept": "application/json",
        "AppKey": os.environ.get("APPKEY")
    }

    main()
