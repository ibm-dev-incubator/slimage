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

from slimage import img_convert
from slimage.tests import base


class TestImgConvert(base.TestCase):

    def test_img_convert_not_vhd_output_path(self):
        self.assertRaises(Exception, img_convert.convert_to_vhd,
                          'fake_path', 'qcow2', 'img.raw')
