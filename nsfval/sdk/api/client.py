import requests
import logging
from requests_toolbelt import MultipartEncoder
import nsfval.sdk.api.settings

log = logging.getLogger(__name__)

base_url = 'http://127.0.0.1:5050/'


def post(endpoint, format, flags='sit', post_file=None, post_path=None, addt_files=None):
    url = base_url + endpoint

    assert post_file or post_path, "Must specify a 'post_file' or 'post_path''"

    post_data = {
        'format': format,
        'source': 'embedded' if post_file else 'local',
        'syntax': 'true' if 's' in flags else 'false',
        'integrity': 'true' if 'i' in flags else 'false',
        'topology': 'true' if 't' in flags else 'false',
    }

    if post_file:
        file_stream = open(post_file, 'rb')
        post_data['file'] = (file_stream.name, file_stream, 'application/octet-stream')

    if addt_files:
        addt_file_streams = list()
        for addt_file in addt_files:
            addt_file_streams.append(open(addt_file, 'rb'))
        post_data['additional_files'] = [(addt_file_stream.name, addt_file_stream, 'application/octet-stream')
                                         for addt_file_stream in addt_file_streams]

    if post_path:
        post_data['path'] = post_path

    encoded_data = MultipartEncoder(post_data)
    post_headers = {'Content-Type': encoded_data.content_type}
    post_response = requests.post(url, headers=post_headers, data=encoded_data)
    return post_response

def get():
    pass