import gc
import os
import unittest

import magic

from test.common_helper import get_config_for_testing, get_test_data_dir
from unpacker.tar_repack import TarRepack


class Test_unpacker_tar_repack(unittest.TestCase):

    def setUp(self):
        self.config = get_config_for_testing()
        self.repack_service = TarRepack(config=self.config)

    def tearDown(self):
        gc.collect()

    def test_tar_repack(self):
        file_path = os.path.join(get_test_data_dir(), 'container/test.zip')
        result = self.repack_service.tar_repack(file_path)
        file_type = magic.from_buffer(result, mime=True)
        self.assertTrue(file_type == 'application/x-gzip' or file_type == 'application/gzip', 'Result is not an tar.gz file')
