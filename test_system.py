import unittest
import subprocess
import os
import shutil
import datetime
import time # Will be used to ensure log file is written

class TestApplicationEndToEnd(unittest.TestCase):

    def setUp(self):
        self.source_data_dir = "SourceData"
        self.logs_dir = "applicationLogs"
        self.today_str = datetime.date.today().strftime("%d%m%Y")
        self.input_file_name = f"input_{self.today_str}.txt"
        self.input_file_path = os.path.join(self.source_data_dir, self.input_file_name)
        self.log_file_name = f"applog_{self.today_str}.log"
        self.log_file_path = os.path.join(self.logs_dir, self.log_file_name)
        
        # Create directories if they don't exist
        if not os.path.exists(self.source_data_dir):
            os.makedirs(self.source_data_dir)
        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir)

    def tearDown(self):
        # Remove directories and their contents
        if os.path.exists(self.source_data_dir):
            shutil.rmtree(self.source_data_dir)
        if os.path.exists(self.logs_dir):
            shutil.rmtree(self.logs_dir)

    def _run_main_py(self):
        # Runs main.py and returns the completed process object
        return subprocess.run(['python', 'main.py'], capture_output=True, text=True)

    def test_successful_execution_with_valid_input(self):
        # 1. Create a sample input file
        sample_content = "Hello world\nhello Python\nWorld of python"
        with open(self.input_file_path, 'w') as f:
            f.write(sample_content)

        # 2. Run main.py
        result = self._run_main_py()

        # 3. Assert exit code
        self.assertEqual(result.returncode, 0, f"main.py exited with {result.returncode}, stderr: {result.stderr}")

        # 4. Assert stdout for word counts
        expected_stdout = "hello : 2\npython : 2\nworld : 2\nof : 1\n"
        # Normalize stdout by stripping trailing newlines and then adding one back for consistent comparison
        actual_stdout = result.stdout.strip() + "\n" 
        self.assertEqual(actual_stdout, expected_stdout)

        # 5. Verify log file creation
        # Add a small delay to ensure the log file is written
        time.sleep(0.1)
        self.assertTrue(os.path.exists(self.log_file_path), f"Log file {self.log_file_path} was not created.")

        # 6. Optionally, check log file content
        with open(self.log_file_path, 'r') as log_f:
            log_content = log_f.read()
        self.assertIn("Pipeline execution Started", log_content)
        self.assertIn("All lines processed", log_content)
        self.assertIn(f"File {self.input_file_path} available!", log_content)


    def test_empty_input_file(self):
        # 1. Create an empty input file
        with open(self.input_file_path, 'w') as f:
            pass # Create empty file

        # 2. Run main.py
        result = self._run_main_py()

        # 3. Assert non-zero exit code
        self.assertNotEqual(result.returncode, 0, "main.py should exit with a non-zero code for empty file.")
        
        # 4. Check stderr for "File is empty" (main.py doesn't print this to stderr, it logs it)
        # main.py prints "File {source_file_path} available!" to stdout even if empty.
        # The actual error "File is empty" is logged.
        # Let's check the log for the error.

        # 5. Verify log file for error message
        time.sleep(0.1) # Ensure log is written
        self.assertTrue(os.path.exists(self.log_file_path), f"Log file {self.log_file_path} was not created for empty input test.")
        with open(self.log_file_path, 'r') as log_f:
            log_content = log_f.read()
        self.assertIn("File is empty", log_content)


    def test_missing_input_file(self):
        # 1. Ensure no input file exists (setUp creates dirs, tearDown removes them)
        if os.path.exists(self.input_file_path):
            os.remove(self.input_file_path) # Should not be necessary due to tearDown

        # 2. Run main.py
        result = self._run_main_py()

        # 3. Assert non-zero exit code
        self.assertNotEqual(result.returncode, 0, "main.py should exit with a non-zero code for missing file.")

        # 4. Check stderr for "File ... not found!" message
        expected_stderr_msg = f"File {self.input_file_path} not found!"
        self.assertIn(expected_stderr_msg, result.stderr)

        # 5. Verify log file for error message
        time.sleep(0.1) # Ensure log is written
        self.assertTrue(os.path.exists(self.log_file_path), f"Log file {self.log_file_path} was not created for missing input test.")
        with open(self.log_file_path, 'r') as log_f:
            log_content = log_f.read()
        self.assertIn(f"File {self.input_file_path} not found!", log_content)


if __name__ == '__main__':
    unittest.main()
