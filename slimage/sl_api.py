# Copyright 2018 IBM Corp.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import SoftLayer as sl
from SoftLayer import config
from swiftclient import client

default_swift_url = 'https://dal05.objectstorage.softlayer.net/auth/v1.0'


class SLImages(object):
    def __init__(self, swift_username, swift_auth_url=default_swift_url):
        self.conf = config.get_client_settings_config_file()
        self.swift_username = swift_username
        self.sl_client = sl.create_client_from_env()
        self.images = sl.ImageManager(self.sl_client)
        self.swift = client.Connection(authurl=swift_auth_url,
                                       user=swift_username,
                                       key=self.conf['api_key'])

    def get_swift_containers(self):
        _, containers = self.swift.get_account()
        return list(containers)

    def upload_file(self, path, name, container):
        self.swift.put_object(container, name, contents=open(path, 'r'))

    def create_image(self, image_name, object_name, container='slimage',
                     cluster='dal05', desc=None, os_type=None):
        if os_type is None:
            os_type = 'DEBIAN_8_64'
        uri_user = self.swift_username.split(':')[0]
        uri = 'swift://%s@%s/%s/%s' % (uri_user, cluster, container,
                                       object_name)
        self.images.import_image_from_uri(image_name, uri, os_code=os_type,
                                          note=desc)
