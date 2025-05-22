# Word Occurance Count

This Python application analyzes text files to determine the frequency of each word. It processes the input by converting all text to lowercase and removing special characters. The program then outputs a list of words and their corresponding counts, sorted in descending order of frequency. Additionally, the application generates log files for each execution, providing a record of its operations. It expects input files to be located in a designated directory and to follow a specific naming convention, as detailed in the 'Assumptions' section.

## Usage

To run the application, execute the following command in your terminal:
```bash
python main.py
```
This script requires Python 3. It uses standard Python libraries, so no separate installation of dependencies is needed.

## Output Format

The script prints the word counts to the standard output. Each line in the output displays a word followed by its frequency, in the format:
```
word: count
```
The list is sorted in descending order based on the word count.

## Logging

The application generates a log file for each execution. These log files record the application's operations, including information about the processed file and any errors encountered.
- Log files are stored in the `applicationLogs` directory.
- Log filenames are date-stamped with the format: `applog_DDMMYYYY.log` (e.g., `applog_16032022.log`).

## Example

Here's a brief example of how the script works.

**Sample Input:**
Consider an input file (`SourceData/input_DDMMYYYY.txt`) with the following content:
```
Hello world
hello python
world of python
```

**Expected Output:**
Running the script with the above input will produce the following output:
```
hello: 2
world: 2
python: 2
of: 1
```

## Testing

The application includes both unit and system tests to ensure its functionality and robustness.

### Unit Tests

Unit tests focus on individual components of the application, primarily functions within `main.py`. These tests are located in the `test_main.py` file.

To run the unit tests, execute the following command in your terminal:
```bash
python -m unittest test_main.py
```

### System Tests

System tests, also known as end-to-end tests, verify the application's behavior as a whole. These tests simulate real-world usage by running the `main.py` script with various inputs and checking the output and log files. The system tests are located in the `test_system.py` file.

To run the system tests, execute the following command in your terminal:
```bash
python -m unittest test_system.py
```
Alternatively, you can run them directly if the file is executable and contains the `unittest.main()` block:
```bash
python test_system.py
```

## Assumptions

The application operates based on the following assumptions:

- **Input File Location:** Input files must be placed in the `SourceData` directory.
- **Input File Naming:** Input files must follow the naming convention: `input_DDMMYYYY.txt` (e.g., `input_16032022.txt`).
- **Word Separation:** Words in the input text are expected to be separated by spaces.
- **Case Handling:** All text is converted to lowercase before word counting to ensure case-insensitive counting.
- **Special Characters:** Special characters are removed from words before counting.
