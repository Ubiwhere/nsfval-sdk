import requests
import logging
import coloredlogs
from requests_toolbelt import MultipartEncoder

log = logging.getLogger(__name__)

def post(url, o_format, flags='sit', post_file=None, post_path=None, addt_files=None):

    assert post_file or post_path, "Must specify a 'post_file' or 'post_path''"

    post_data = {
        'format': o_format,
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