import os

class FileFeed():
    """The FileFeed class determines appropriate file paths to use for retrieving images
       and for saving 'positive' and 'negative' images while avoiding duplicating work
       in the event that user completes classification in multiple sessions. To avoid duplication
       the same positive_directory and negative_directory should always be used for one batch"""

    def __init__(self, existing_directory, positive_directory, negative_directory):
        """Saves file locations to instance variables and determines the appropriate files 
           for editing, based on removing any that have already been edited"""

        self.existing_directory = existing_directory
        self.positive_directory = positive_directory
        self.negative_directory = negative_directory
        self.index = 0

        # Retrieves complete list of files to be edited
        list_of_files = []
        file_names = []
        walker = iter(os.walk(self.existing_directory))
        next(walker)
        for dir, _, _ in walker:
            files = [dir + "/" +  file for file in os.listdir(dir)]            
            list_of_files.extend(files)
            file_names.extend(os.listdir(dir))

        # Determines which files have already been edited
        list_of_processed_files = []
        processed_file_names = []
        walker = iter(os.walk(self.positive_directory))
        next(walker)
        for dir, _, _ in walker:
            files = [dir + "/" +  file for file in os.listdir(dir)]            
            list_of_processed_files.extend(files)
            processed_file_names.extend(os.listdir(dir))

        # List of files to edit does not include those that have already been edited
        good_names = set(file_names) - set(processed_file_names)
        self.list_of_files = [f for i, f in enumerate(list_of_files) if file_names[i] in good_names] 


    def next_file(self):
        self.index += 1
        return self.list_of_files[self.index - 1]


    def get_negative_file(self):
        """Returns a tuple containing the absolute directory (0) and filename (1)
        where a negative file should be saved for the corresponding image/index. This 
        preserves folder and file identity from the original directory, but now in the
        'negative' directory."""
        files = self.list_of_files[self.index].split("/")
        try:
            os.stat(self.negative_directory+files[-2])
        except:
            os.mkdir(self.negative_directory+files[-2])
        return ("{}{}/".format(self.negative_directory, files[-2]), files[-1])


    def get_positive_file(self):
        """Returns same items as get_negative_file except for the positive directory"""
        files = self.list_of_files[self.index].split("/")
        try:
            os.stat(self.positive_directory+files[-2])
        except:
            os.mkdir(self.positive_directory+files[-2])
        return ("{}{}/".format(self.positive_directory, files[-2]), files[-1])