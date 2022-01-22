# open file in read mode
from csv import reader
from typing import Tuple
from typing import List
from typing import Dict
from datetime import *
import os
import os.path
import operator
from heapq import merge
import multiprocessing
from threading import Thread, Lock
import time
from dateutil import rrule


def list_taxi_files(folder: str) -> List[str]:
    taxi_files_raw: List[str] = os.listdir(folder)
    taxi_files: List[str] = []
    for file_name in taxi_files_raw:
        if 'tripdata' in os.path.basename(file_name).split('.')[0]:
            taxi_files.append(file_name)
    return taxi_files


def list_taxi_month(files: List[str], taxi_type: str) -> List[datetime]:
    taxi_type_month: List[datetime] = []
    for file in files:
        if file.startswith(taxi_type):
            datestring_csv: str = file.split('_')[2]
            datestring: str = datestring_csv.split('.')[0]
            output_datetime: datetime = datetime.strptime(datestring, "%Y-%m")
            taxi_type_month.append(output_datetime)
    return taxi_type_month


def end_of_month(date_in: datetime) -> datetime:
    end_month = datetime(date_in.year, date_in.month, 1)
    over_one_month_later = end_month + timedelta(days=33)
    end_last_month = datetime(1, 1, 1)
    first: bool = True
    for dt in rrule.rrule(rrule.MONTHLY, dtstart=end_month, until=over_one_month_later):
        if first:
            first = False
            continue
        else:
            end_last_month = dt - timedelta(seconds=1)
            break
    return end_last_month


class TaxiData:

    def get_date_files(self, year: int, month: int) -> Dict[str, List[datetime]]:
        taxi_color_types_filter: Dict[str, List[datetime]] = {}
        request_datetime: datetime = datetime(year, month, 1)
        for taxi_colors, taxi_times in self.taxi_color_types_times.items():
            if request_datetime in taxi_times:
                if not (taxi_colors in taxi_color_types_filter.keys()):
                    taxi_color_types_filter[taxi_colors] = []
                taxi_color_types_filter[taxi_colors].append(request_datetime)

        return taxi_color_types_filter

    def __load_csv_multithread(self, build_file_name: str, taxi_color_request: str) -> None:
        self.iomutex.acquire()
        with open(build_file_name, 'r') as read_obj:
            time_csv: str = os.path.basename(build_file_name).split('_')[2]
            time_string: str = time_csv.split('.')[0]
            time_month: datetime = datetime.strptime(time_string, "%Y-%m")
            # pass the file object to reader() to get the reader object
            csv_reader = reader(read_obj)
            self.iomutex.release()
            # Get all rows of csv from csv_reader object as list of tuples
            list_of_tuples_load = list(map(tuple, csv_reader))

            list_of_tuples_load_typed: List[Tuple[int, datetime, datetime, int, float, int, str, int,
                                                  int, int, float, float, float, float, float, float,
                                                  float, float, str]] = []

            count: int = 0
            for tup in list_of_tuples_load:
                if count == 0:
                    output_tup1: Tuple[str, str, str, str, str, str, str, str, str, str, str, str,
                                       str, str, str, str, str, str, str]
                    if taxi_color_request == 'yellow':
                        """
                        VendorID
                        tpep_pickup_datetime
                        tpep_dropoff_datetime
                        passenger_count
                        trip_distance
                        RatecodeID
                        store_and_fwd_flag
                        PULocation
                        DOLocation
                        payment_type
                        fare_amount
                        extra
                        mta_tax
                        tip_amount
                        tolls_amount
                        improvement_surcharge
                        total_amount
                        congestion_surcharge
                        """
                        output_tup1 = (str(tup[0]),
                                       str(tup[1])[5:],
                                       str(tup[2])[5:],
                                       str(tup[3]),
                                       str(tup[4]),
                                       str(tup[5]),
                                       str(tup[6]),
                                       str(tup[7]),
                                       str(tup[8]),
                                       str(tup[9]),
                                       str(tup[10]),
                                       str(tup[11]),
                                       str(tup[12]),
                                       str(tup[13]),
                                       str(tup[14]),
                                       str(tup[15]),
                                       str(tup[16]),
                                       str(tup[17]),
                                       str('TaxiColor'))
                    else:
                        output_tup1 = (str(tup[0]),
                                       str(tup[1])[5:],
                                       str(tup[2])[5:],
                                       str(tup[7]),
                                       str(tup[8]),
                                       str(tup[4]),
                                       str(tup[3]),
                                       str(tup[5]),
                                       str(tup[6]),
                                       str(tup[17]),
                                       str(tup[9]),
                                       str(tup[10]),
                                       str(tup[11]),
                                       str(tup[12]),
                                       str(tup[13]),
                                       str(tup[15]),
                                       str(tup[16]),
                                       str(tup[19]),
                                       str('TaxiColor'))
                    self.header: Tuple[str, str, str, str, str, str, str, str, str, str, str, str,
                                       str, str, str, str, str, str, str] = output_tup1
                else:
                    pickup_time: datetime = datetime.strptime(str(tup[1]), "%Y-%m-%d %H:%M:%S")
                    if not (pickup_time.year == time_month.year and pickup_time.month == time_month.month):
                        continue
                    output_tup: Tuple[int, datetime, datetime, int, float, int, str, int,
                                      int, int, float, float, float, float, float, float,
                                      float, float, str]

                    vendor_fix: int = 0
                    passenger_count_fix: int = 0
                    ratecodeid_fix: int = 0
                    store_and_fwd_flag_fix: str = '?'
                    payment_type_fix: int = 0
                    congestion_surcharge_fix: float = 0
                    if len(tup[0]) != 0:
                        vendor_fix = int(tup[0])
                    if taxi_color_request == 'yellow':
                        if len(tup[3]) != 0:
                            passenger_count_fix = int(tup[3])
                        if len(tup[5]) != 0:
                            ratecodeid_fix = int(tup[5])
                        if len(tup[6]) != 0:
                            store_and_fwd_flag_fix = str(tup[6])
                        if len(tup[9]) != 0:
                            payment_type_fix = int(tup[9])
                        if len(tup[17]) != 0:
                            congestion_surcharge_fix = float(tup[17])

                        output_tup = (vendor_fix,
                                      pickup_time,
                                      datetime.strptime(str(tup[2]), "%Y-%m-%d %H:%M:%S"),
                                      passenger_count_fix,
                                      float(tup[4]),
                                      ratecodeid_fix,
                                      store_and_fwd_flag_fix,
                                      int(tup[7]),
                                      int(tup[8]),
                                      payment_type_fix,
                                      float(tup[10]),
                                      float(tup[11]),
                                      float(tup[12]),
                                      float(tup[13]),
                                      float(tup[14]),
                                      float(tup[15]),
                                      float(tup[16]),
                                      congestion_surcharge_fix,
                                      str('yellow'))
                    else:
                        if len(tup[7]) != 0:
                            passenger_count_fix = int(tup[7])
                        if len(tup[4]) != 0:
                            ratecodeid_fix = int(tup[4])
                        if len(tup[3]) != 0:
                            store_and_fwd_flag_fix = str(tup[3])
                        if len(tup[17]) != 0:
                            payment_type_fix = int(tup[17])
                        if len(tup[19]) != 0:
                            congestion_surcharge_fix = float(tup[19])

                        output_tup = (vendor_fix,
                                      pickup_time,
                                      datetime.strptime(str(tup[2]), "%Y-%m-%d %H:%M:%S"),
                                      passenger_count_fix,
                                      float(tup[8]),
                                      ratecodeid_fix,
                                      store_and_fwd_flag_fix,
                                      int(tup[5]),
                                      int(tup[6]),
                                      payment_type_fix,
                                      float(tup[9]),
                                      float(tup[10]),
                                      float(tup[11]),
                                      float(tup[12]),
                                      float(tup[13]),
                                      float(tup[15]),
                                      float(tup[16]),
                                      congestion_surcharge_fix,
                                      str('green'))
                    list_of_tuples_load_typed.append(output_tup)
                count += 1
            # sort to pickup time
            list_of_tuples_load_typed = sorted(list_of_tuples_load_typed, key=operator.itemgetter(1))
            self.datamutex.acquire()
            self.data = list(merge(self.data, list_of_tuples_load_typed, key=operator.itemgetter(1)))
            self.datamutex.release()

    def load_add_available(self, available: Dict[str, List[datetime]]) -> bool:
        for taxi_color_request, times_request in available.items():
            if taxi_color_request in self.taxi_color_types_times.keys():
                if set(times_request).issubset(self.taxi_color_types_times.get(taxi_color_request)):
                    for times in times_request:
                        if (taxi_color_request in self.already_loaded.keys()) and \
                                (times in self.already_loaded[taxi_color_request]):
                            continue
                        build_month: str = str(times.month)
                        while len(build_month) <= 1:
                            build_month = str(0) + build_month
                        build_file_name: str = self.base_folder + taxi_color_request + '_tripdata_' + str(
                            times.year) + str('-') + build_month + '.csv'

                        # create maximum number of threads with one master and rest workers
                        # don't reserve master thread for more speed
                        """
                                                while True:
                            newthreadlist: List[Thread] = []
                            for t in self.threadlist:
                                if t.is_alive():
                                    newthreadlist.append(t)
                            self.threadlist = newthreadlist
                            if len(self.threadlist) < multiprocessing.cpu_count():
                                break
                            else:
                                time.sleep(0.2)
                        """
                        self.__load_csv_multithread(build_file_name, taxi_color_request)
                        """
                        self.threadlist.append(Thread(target=self.__load_csv_multithread,
                                                      args=(build_file_name, taxi_color_request)))
                        self.threadlist[-1].start()
                        """

                        if not (taxi_color_request in self.already_loaded.keys()):
                            self.already_loaded[taxi_color_request] = []
                        self.already_loaded[taxi_color_request].append(times)
                else:
                    return False
            else:
                return False
        # join all threads
        """
                for t in self.threadlist:
            t.join()
        self.threadlist = []
        """

        return True

    def load_available(self, available: Dict[str, List[datetime]]) -> bool:
        self.data = []
        self.already_loaded = {}
        return self.load_add_available(available)

    def get_minimum_available_pickup_time(self, taxi_color: str = '') -> datetime:
        # get minimum month of available files
        first_key: str = ''
        for some_key in self.taxi_color_types_times.keys():
            first_key = some_key
            break
        min_d: datetime = self.taxi_color_types_times[first_key][0]
        if taxi_color == '':
            for times in self.taxi_color_types_times.values():
                for time_taxi in times:
                    if time_taxi < min_d:
                        min_d = time_taxi
        else:
            for time_taxi in self.taxi_color_types_times[taxi_color]:
                if time_taxi < min_d:
                    min_d = time_taxi
        # load all minimum month files and get minimum time
        self.load_add_available(self.get_date_files(min_d.year, min_d.month))
        self.datamutex.acquire()
        min_d = self.data[0][1]
        self.datamutex.release()
        for tup in self.data:
            if tup[1] < min_d:
                min_d = tup[1]

        return min_d

    def get_maximum_available_pickup_time(self, taxi_color: str = '') -> datetime:
        # get minimum month of available files
        first_key: str = ''
        for some_key in self.taxi_color_types_times.keys():
            first_key = some_key
            break
        max_d: datetime = self.taxi_color_types_times[first_key][0]
        if taxi_color == '':
            for times in self.taxi_color_types_times.values():
                for time_taxi in times:
                    if time_taxi > max_d:
                        max_d = time_taxi
        else:
            for time_taxi in self.taxi_color_types_times[taxi_color]:
                if time_taxi > max_d:
                    max_d = time_taxi
        # load all minimum month files and get minimum time
        self.load_add_available(self.get_date_files(max_d.year, max_d.month))
        self.datamutex.acquire()
        max_d = self.data[0][1]
        self.datamutex.release()
        for tup in self.data:
            if tup[1] > max_d:
                max_d = tup[1]

        return max_d

    # start and an optional 'end'
    def load_range(self, start: datetime, end: datetime) -> bool:
        if start > end:
            print('Start was older than end, switching start and and of range now!')
            tmp = start
            start = end
            end = tmp
        start_month: datetime = datetime(start.year, start.month, 1)
        end_month: datetime = datetime(end.year, end.month, 1)
        if start_month < self.min_time:
            raise ValueError('Start month was smaller than known minimum month.')
        if start_month > self.max_time:
            raise ValueError('Start month was greater than known maximum month.')
        if end_month < self.min_time:
            raise ValueError('End month was smaller than known minimum month.')
        if end_month > self.max_time:
            raise ValueError('End month was greater than known maximum month.')

        feedback: bool = True
        if not (self.min_is_loaded is not None and self.max_is_loaded is not None and self.min_is_loaded <= start
                and end <= self.max_is_loaded):
            # load not already loaded month
            month_to_load: Dict[str: List[datetime]] = {}
            total_reload: bool = True
            for dt in rrule.rrule(rrule.MONTHLY, dtstart=start_month, until=end_month):
                available_files = self.get_date_files(dt.year, dt.month)
                for color, color_list in self.already_loaded.items():
                    for color_av, color_list_av in available_files.items():
                        if color != color_av:
                            continue
                        if not set(color_list_av).issubset(set(color_list)):
                            if not (color_av in month_to_load.keys()):
                                month_to_load[color_av] = []
                            for time_av in color_list_av:
                                month_to_load[color_av].append(time_av)
                        else:
                            total_reload = False
            # on total reload just load_available, else filter from the first day of the first month to the last second
            # of the last month and then load_add_available

            if total_reload:
                feedback = self.load_available(month_to_load)
            else:
                # filter down everything that is not officially loaded
                for color_al, time_list_al in self.already_loaded.items():
                    new_data: List[
                        Tuple[int, datetime, datetime, int, float, int, str, int, int, int, float, float, float, float,
                              float, float, float, float, str]] = []
                    if len(time_list_al) == 0:
                        for entry in self.data:
                            if not (entry[18] == color_al):
                                new_data.append(entry)
                    else:
                        min_month = min(time_list_al)
                        max_month = end_of_month(max(time_list_al))
                        for entry in self.data:
                            if (entry[18] != color_al) or not (entry[1] < min_month or entry[1] > max_month):
                                new_data.append(entry)
                    self.data = new_data

                # load missing months
                feedback = self.load_add_available(month_to_load)
        # when we now filter with start and end within the first and last month we check if we deleted values
        # on deletion the month is incomplete is does not count to self.already loaded
        month_incomplete: List[datetime] = []
        new_data: List[Tuple[int, datetime, datetime, int, float, int, str, int, int, int, float, float, float, float,
                             float, float, float, float, str]] = []
        for entry in self.data:
            if entry[1] < start or entry[1] > end:
                month_here = datetime(entry[1].year, entry[1].month, 1)
                if not (month_here in month_incomplete):
                    month_incomplete.append(month_here)
            else:
                new_data.append(entry)
        self.data = new_data
        # remove incomplete month from already_loaded
        for incom in month_incomplete:
            for color_al, time_list_al in self.already_loaded.items():
                if incom in time_list_al:
                    self.already_loaded[color_al].remove(incom)
        self.min_is_loaded = self.data[0][1]
        self.max_is_loaded = self.data[-1][1]
        return feedback

    def __init__(self, base: str):
        self.min_is_loaded = None
        self.max_is_loaded = None
        self.datamutex: Lock() = Lock()
        self.iomutex: Lock() = Lock()
        # self.threadlist: List[Thread] = []
        self.header = None
        self.base_folder: str = base
        # last tuple entry is taxi color
        self.data: List[Tuple[int, datetime, datetime, int, float, int, str, int, int, int,
                              float, float, float, float, float, float, float, float, str]] = []
        # get available files
        self.taxi_files: List[str] = list_taxi_files(self.base_folder)
        # read available month to be read instantly
        self.taxi_color_types_times: Dict[str, List[datetime]] = {'yellow': list_taxi_month(self.taxi_files, 'yellow'),
                                                                  'green': list_taxi_month(self.taxi_files, 'green')}
        self.already_loaded: Dict[str, List[datetime]] = {}
        self.min_time: datetime = self.get_minimum_available_pickup_time()
        self.max_time: datetime = self.get_maximum_available_pickup_time()
