
from slimage import img_convert
from slimage.tests import base


class TestImgConvert(base.TestCase):

    def test_img_convert_not_vhd_output_path(self):
        self.assertRaises(Exception, img_convert.convert_to_vhd,
                          'fake_path', 'qcow2', 'img.raw')
