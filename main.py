"""
    This python application reads a text file and counts occurences of each word,
    print output in desceding order of count of occureneces.
    Considerations :
        -Files are coming in SourceData folder
        -File names will be appended with current date
        -Words are sperated using space
        -Entire text will be converted to lower case first before checking the count.
        -Removing any special characters.
"""
import sys
import re
import logging
from datetime import date
"""creating logging instance which will generate application log for each run in applicationLogs folder"""
log_file_date = date.today().strftime("%d%m%Y")
log_file_name = 'applicationLogs/applog_' + str(log_file_date) + '.txt'
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=log_file_name,
                    filemode='w')
logging.info("Pipeline execution Started")


"""get_file_name function is used to check file avaialabilty in source folder"""


def get_file_name(source_directory, source_file):
    from datetime import date
    """ Assuming new files will come with current date appended to it. """
    file_date = date.today().strftime("%d%m%Y")
    source_file_path = source_directory + '/' + source_file + '_' + str(file_date) + '.txt'
    logging.info("Checking availability of file " + source_file_path)
    try:
        f = open(source_file_path, 'r')  # or os.remove(path)
        logging.info(f"File {source_file_path} available!")
        print(f"File {source_file_path} available!", file=sys.stdout)
        return f
    except FileNotFoundError as e:
        logging.error(f"File {source_file_path} not found! {sys.exc_info()[0]}")
        print(f"File {source_file_path} not found! {sys.exc_info()[0]}", file=sys.stderr)
        sys.exit()


def main():
    text = get_file_name(source_directory='SourceData', source_file='input')
    """Creating empty python dictionary to keep key value pair"""
    key_value = dict()
    """Reading each line in text file"""
    logging.info("Looping through each line of text file")
    num_lines = 0
    for line in text:
        num_lines = num_lines+1
        logging.info(f"Processing Started for Line Number - {num_lines}")
        """Refomratting/standardize text - trimming space, changing to lowercase and replacing 
        multiple spaces to single space"""
        line = line.strip()
        line = line.lower()
        line = re.sub('\s+', ' ', line)
        words = line.split(" ")
        """Creating dictionary with each word as key, and value is incremented for multiple occurance else 1"""
        for word in words:
            # Removing special chracter
            word = re.sub('[^A-Za-z0-9]+', '', word)
            if word in key_value:
                key_value[word] = key_value[word] + 1
            else:
                key_value[word] = 1
        logging.info(f"Processing Completed for Line Number - {num_lines}")
    logging.info("All lines processed and dictionary is updated with updated count")
    # Print the contents of dictionary in descending order
    sorted_dict = dict(sorted(key_value.items(), key=lambda item: item[1], reverse=True))
    for key in list(sorted_dict.keys()):
        print(key, ":", sorted_dict[key])


if __name__ == '__main__':
    main()
