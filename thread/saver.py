import os
import shutil
import time
import datetime
import math
from PyQt5.QtCore import QThread, pyqtSignal
import itertools

class SaverThread(QThread):
    """ Saver class that perform the saving actions """

    update_percentage_signal = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self):
        """ Initialize the thread """
        QThread.__init__(self)

    def set_path_group_list(self, path_group_list):
        """ Set the path_group_list to save """
        self.path_group_list = path_group_list

    def run(self):
        """ For every group of path in path_group_list copy the everything in the input folder to the output folder """

        start_time = time.time()
        for path_group in self.path_group_list:
            input_path, output_path = path_group

            if not os.path.isdir(input_path) or not os.path.isdir(output_path):
                print("directory not existing, skipping it")
                continue

            self.total_size = sum(itertools.chain(*((os.path.getsize(os.path.join(root, file)) for file in files) for root, dirs, files in os.walk(input_path, topdown=False))))
            self.size_transfered = 0
            self.previous_percentage = 0
            number_of_files = sum((len(files) for root, dirs, files in os.walk(path, topdown=False)))

            self._print_info(input_path, self.total_size, number_of_files)

            self._copy(input_path, output_path)
            self._delete_old_files(input_path, output_path)
        
        def _format_date(date):
            hours, minutes, seconds = date
            return "{}h {}m {}s".format(hours.zfill(2), minutes.zfill(2), seconds.zfill(2))

        if time.time()-start_time < 24*3600:
            delta_time = str(datetime.timedelta(seconds=time.time()-start_time))
            print("Save finished in", _format_date(delta_time.split(":")))
        else:
            delta_time = str(datetime.timedelta(seconds=time.time()-start_time))
            print("Save finished in",  _format_date(delta_time.slit(",")[1][1:].split(":")))
        
    def _print_info(self, path, size, number_of_files):
        def format_size(size):
            prefix = ["", "k", "M", "G", "T", "P"]
            if size != 0:
                return "{} {}B".format(size/1000**int(math.log(size, 1000)), prefix[int(math.log(size, 1000))])
            else:
                return "0 B"

        print("INFO:")
        print("Path:", path)
        print("Number of files:", number_of_files)
        print("Size:", format_size(size))

    def _copy(self, input_path, output_path):
        """ Copies recursively everything in the folder of the input_path to the folder of the ouput path """
        
        for file in os.listdir(input_path):
            if os.path.isfile(input_path + "/" +  file):
                if os.path.isfile(output_path + "/" + file):
                    modif_time_original_file = os.path.getmtime(input_path + "/" +  file)
                    modif_time_saved_file = os.path.getmtime(output_path + "/" + file)
                    if modif_time_original_file > modif_time_saved_file:
                        shutil.copy2(input_path + "/" + file, output_path)
                else:
                    shutil.copy2(input_path + "/" + file, output_path)

                self.size_transfered += os.path.getsize(input_path + "/" + file)
                percentage = int(self.size_transfered/self.total_size*100)

                if percentage != self.previous_percentage:
                    self.update_percentage_signal.emit(percentage)

                self.prevous_percentage = percentage

            elif os.path.isdir(input_path + "/" + file):
                if not os.path.isdir(output_path + "/" + file):
                    os.mkdir(output_path + "/" + file)
                self._copy(input_path + "/" + file, output_path + "/" + file)
        self._delete_old_files(input_path, output_path)
        self.finished.emit()
        return True

    def _delete_old_files(self, input_path, output_path):
        """ Delete the files that are in the ouput directory but have been removed from the input directory """
        
        input_file_list = os.listdir(input_path)
        output_file_list = os.listdir(output_path)
        if output_file_list != input_file_list:
            for file in output_file_list:
                if not file in input_file_list:
                    os.remove(output_path + "/" + file)
