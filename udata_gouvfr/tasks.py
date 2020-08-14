import mongoengine
import requests

from collections import defaultdict
from flask import current_app

from udata.commands import success, error
from udata.core.dataset.models import Dataset
from udata.tasks import job

from udata_gouvfr import APIGOUVFR_EXTRAS_KEY


def get_dataset(id_or_slug):
    obj = Dataset.objects(slug=id_or_slug).first()
    return obj or Dataset.objects.get(id=id_or_slug)


def process_dataset(d_id, apis):
    try:
        dataset = get_dataset(d_id)
    except (Dataset.DoesNotExist, mongoengine.errors.ValidationError):
        return error(f'Dataset {d_id} not found')
    dataset.extras[APIGOUVFR_EXTRAS_KEY] = apis
    dataset.save()
    success(f'Imported {len(apis)} API(s) for {str(dataset)}')


@job("apigouvfr-load-apis")
def apigouvfr_load_apis(self):
    '''Load dataset-related APIs from api.gouv.fr'''
    r = requests.get(current_app.config['APIGOUVFR_URL'])
    r.raise_for_status()

    apis = r.json()
    datasets_apis = defaultdict(list)
    for api in apis:
        # strictly non open APIs, ignore
        if api['is_open'] == -1:
            continue
        d_ids = api.pop('datagouv_uuid', [])
        for d_id in d_ids:
            if api not in datasets_apis[d_id]:
                datasets_apis[d_id].append(api)

    for d_id, d_apis in datasets_apis.items():
        process_dataset(d_id, d_apis)

    success('Done.')
