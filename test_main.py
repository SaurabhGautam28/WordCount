import unittest
from unittest.mock import patch, MagicMock
import main
import os
import datetime
import sys
import io

class TestGetFileName(unittest.TestCase):

    def setUp(self):
        self.source_directory = "SourceData"
        self.source_file_base = "input"
        # Create SourceData directory if it doesn't exist
        if not os.path.exists(self.source_directory):
            os.makedirs(self.source_directory)

    def tearDown(self):
        # Clean up SourceData directory if it was created and is empty
        # More specific file cleanup will be done in the test_get_file_name_exists
        if hasattr(self, 'expected_file_path') and os.path.exists(self.expected_file_path):
             if os.path.exists(self.expected_file_path): # check again before removing
                os.remove(self.expected_file_path)
        
        if os.path.exists(self.source_directory) and not os.listdir(self.source_directory):
            os.rmdir(self.source_directory)


    @patch('main.date')
    def test_get_file_name_exists(self, mock_date):
        # Mock datetime.date.today() to return a fixed date
        fixed_date = datetime.date(2023, 10, 26)
        mock_date.today.return_value = fixed_date
        
        # Construct the expected filename
        date_str = fixed_date.strftime("%d%m%Y")
        self.expected_file_path = os.path.join(self.source_directory, f"{self.source_file_base}_{date_str}.txt")

        # Create the dummy file
        with open(self.expected_file_path, 'w') as f:
            f.write("Test content")

        # Call get_file_name
        returned_file_obj = main.get_file_name(self.source_directory, self.source_file_base)

        # Assertions
        self.assertIsNotNone(returned_file_obj, "get_file_name should return a file object, not None")
        self.assertTrue(hasattr(returned_file_obj, 'read'), "Returned object should have a 'read' method")
        self.assertEqual(returned_file_obj.name, self.expected_file_path, "File object name should match expected path")

        # Clean up
        if returned_file_obj:
            returned_file_obj.close()
        # File removal is now handled in tearDown to ensure it runs even if asserts fail

    @patch('main.date')
    @patch('main.sys.exit') # Mock sys.exit to prevent test termination and check if it's called
    def test_get_file_name_not_found(self, mock_sys_exit, mock_date):
        # Mock datetime.date.today() to return a date for which no file will exist
        fixed_date = datetime.date(2023, 10, 27) # Different date
        mock_date.today.return_value = fixed_date

        # Construct the non-existent filename
        date_str = fixed_date.strftime("%d%m%Y")
        non_existent_file_path = os.path.join(self.source_directory, f"{self.source_file_base}_{date_str}.txt")
        
        # Ensure the file does not exist before calling
        if os.path.exists(non_existent_file_path):
            os.remove(non_existent_file_path) # Should not happen based on date, but good practice

        main.get_file_name(self.source_directory, self.source_file_base)
        mock_sys_exit.assert_called_once()


class TestMainFunctionality(unittest.TestCase):

    @patch('main.get_file_name')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_basic_word_count(self, mock_stdout, mock_get_file_name):
        # Mock get_file_name to return an io.StringIO object
        mock_file_content = "hello world hello"
        mock_file_object = io.StringIO(mock_file_content)
        # Simulate the behavior of a real file object for read(1)
        mock_file_object.read = lambda size: mock_file_content[0:size] if size == 1 else mock_file_content 
        # Simulate seek for multiple reads if necessary, and name attribute
        mock_file_object.seek = lambda pos: None 
        mock_file_object.name = "mock_input.txt"
        # Crucially, when get_file_name returns the file, the main function iterates over it.
        # StringIO objects are directly iterable line by line.
        # We need to ensure `text.read(1)` works as expected in main()
        # For the iteration `for line in text:`, StringIO works fine.

        # We need to make a copy for the `read(1)` check, because read(1) consumes the first char
        # and then the iteration will miss it.
        # Or, more simply, make the mock_file_object itself, then make a "copy" for read(1)
        # then reset it for the iteration.

        # Create a MagicMock that wraps StringIO for the read(1) check
        # and then provides the original StringIO for iteration.
        
        # Let's simplify: main.py's `text.read(1)` checks if file is empty.
        # Then it iterates `for line in text:`. StringIO handles this fine.
        # We just need to make sure the read(1) doesn't consume the content needed for iteration.
        # A simple way is to reset the StringIO's cursor.
        
        # For the read(1) check
        mock_get_file_name.return_value = io.StringIO(mock_file_content)

        main.main()
        
        expected_output = "hello : 2\nworld : 1\n"
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('main.get_file_name')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_case_insensitivity(self, mock_stdout, mock_get_file_name):
        mock_file_content = "Hello hello HeLlO"
        mock_get_file_name.return_value = io.StringIO(mock_file_content)
        
        main.main()
        
        expected_output = "hello : 3\n"
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('main.get_file_name')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_special_character_removal(self, mock_stdout, mock_get_file_name):
        mock_file_content = "word1! word2. word1?"
        mock_get_file_name.return_value = io.StringIO(mock_file_content)
        
        main.main()
        
        expected_output = "word1 : 2\nword2 : 1\n" # Assuming 'word1?' becomes 'word1'
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch('main.get_file_name')
    @patch('main.sys.exit') # Mock sys.exit
    def test_empty_file_handling(self, mock_sys_exit, mock_get_file_name):
        # Mock get_file_name to return an empty StringIO object
        mock_empty_file = io.StringIO("")
        mock_get_file_name.return_value = mock_empty_file
        
        main.main()
        
        mock_sys_exit.assert_called_once()

    @patch('main.get_file_name')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_correct_sorting_of_output(self, mock_stdout, mock_get_file_name):
        mock_file_content = "apple banana apple orange banana apple"
        # Expected counts: apple: 3, banana: 2, orange: 1
        mock_get_file_name.return_value = io.StringIO(mock_file_content)
        
        main.main()
        
        expected_output = "apple : 3\nbanana : 2\norange : 1\n"
        self.assertEqual(mock_stdout.getvalue(), expected_output)

if __name__ == '__main__':
    unittest.main()
