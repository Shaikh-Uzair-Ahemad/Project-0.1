import os


class CreateFile:
    def __init__(self, file_name):
        self.file_name = file_name

        # Create Directory
        self.dir_name = os.path.dirname(self.file_name)
        if not os.path.exists(self.dir_name):
            os.makedirs(self.dir_name)

        #  Create file with Name Today Date
        self.file = open(self.file_name, 'w')
        header = ['Name', 'Time', 'Date']
        sep = ","
        self.file.write(sep.join(header))
        self.file.close()
