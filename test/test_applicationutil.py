import unittest
import os
import shutil
import tempfile
from applicationutil import *

class TestApplicationUtil(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        self.zero_len_file = os.path.join(self.test_dir, "zero.txt") 
        with open(self.zero_len_file,mode='w') as f:
            pass

        self.file_with_text = os.path.join(self.test_dir, "file_with_text.txt") 
        with open(self.file_with_text, mode='w') as f:
            f.writelines ('sdf sdsdg sdg sgrsg')
        # print (self.test_dir)
        # print(self.zero_len_file)

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    def test_test_file_folder_exists(self):
        self.assertTrue (os.path.exists(self.test_dir))
        self.assertTrue(os.path.exists(self.zero_len_file))

    def test_zero_len_file_exists(self):
        self.assertTrue (os.path.exists(self.test_dir))
        self.assertTrue(os.path.exists(self.zero_len_file))
        self.assertEqual (os.stat(self.zero_len_file).st_size,0)

    def test_file_with_data_exists(self):
        self.assertTrue (os.path.exists(self.test_dir))
        self.assertTrue(os.path.exists(self.file_with_text))
        self.assertNotEqual  (os.stat(self.file_with_text).st_size,0)

    def test_remove_zero_byte_file(self):
        remove_zero_byte_file (self.test_dir)
        self.assertTrue(os.path.exists(self.file_with_text))
        self.assertFalse(os.path.exists(self.zero_len_file))



    if __name__ == '__main__':
        unittest.main()
    