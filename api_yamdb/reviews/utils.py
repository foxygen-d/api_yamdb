import os
import csv
from typing import Dict, List
from django.conf import settings


def get_csv_data(source) -> List[Dict]:

    base_dir = settings.BASE_DIR
    with open(os.path.join(base_dir, f'static/data/{source}.csv'), 'r') as file:
        csv_dict = csv.DictReader(file)
        to_db = [
            {attr: row.get(attr) for attr in row} for row in csv_dict
        ]
    return to_db
