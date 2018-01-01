#!/usr/bin/env python

"""
Convert an Everlance CSV format to a MileIQ CSV format

- the MileIQ CSV format can be imported to QuickBooks Self Employed
"""
import collections
import csv
from datetime import datetime
# import math
import re
import sys
import traceback

# https://www.irs.gov/newsroom/2017-standard-mileage-rates-for-business-and-medical-and-moving-announced
IRS_MILES = 0.535


class Everlance:
    """An Everlance CSV data structure"""



    # Deduction, Miles, From, To, Date, Purpose, Income Source, Map Image URL,
    # Auto Detected?, Notes, Vehicle, Time Started, Time Ended, Time Zone, Photo URL,
    # From Full Address, To Full Address
    def __init__(self, deduction, miles, from_loc, to_loc, date, purpose, income_source, map_url,
                 auto_detection, notes, vehicle, time_started, time_ended, time_zone, photo_url,
                 from_address, to_address):
        self.data = collections.OrderedDict()
        self.data["deduction"] = deduction
        self.data["miles"] = miles
        self.data["from_loc"] = from_loc
        self.data["to_loc"] = to_loc
        self.data["date"] = date
        self.data["purpose"] = purpose
        self.data["income_source"] = income_source
        self.data["map_url"] = map_url
        self.data["auto_detection"] = auto_detection
        self.data["notes"] = notes
        self.data["vehicle"] = vehicle
        self.data["time_started"] = time_started
        self.data["time_ended"] = time_ended
        self.data["time_zone"] = time_zone
        self.data["photo_url"] = photo_url
        self.data["from_address"] = from_address
        self.data["to_address"] = to_address

    def to_csv(self):
        # wrap all the values in quotes because addresses contain commas
        return ''.join(['"', '","'.join(self.data.values()), '"'])

    def to_mileIQ(self):
        # (start_date, end_date, category, start, stop, miles,
        # miles_value=None, parking=None, tolls=None, total=None,
        # vehicle=None, purpose=None, notes=None):
        from_loc = self.data["from_address"] or self.data["from_loc"]
        to_loc = self.data["to_address"] or self.data["to_loc"]
        category = "Business"
        if self.data["purpose"] == "Personal":
            category = "Personal"
        miles = self.data["miles"]
        miles_value = str(float(miles) * IRS_MILES)
        data = [
            self.datetime_start(), self.datetime_end(),
            category,
            from_loc, to_loc,
            miles, miles_value, "0", "0", miles_value,
            self.data["vehicle"], category, self.data["income_source"]
        ]
        return MileIQ(*data)

    def datetime(self, time):
        # dates are "YYYY-MM-DD"
        # times are "HH:MM AM/PM" by zone
        # e.g. "2017-01-07 08:57AM"
        date = self.data["date"]
        date_time = "%s %s" % (date, time)
        date_time = datetime.strptime(date_time, '%Y-%m-%d %I:%M%p')
        return date_time.strftime('%m/%d/%Y %H:%M')

    def datetime_start(self):
        time = self.data["time_started"].replace(" ", "")
        if time is None or time == "":
            time = "08:00AM"
        return self.datetime(time)

    def datetime_end(self):
        time = self.data["time_ended"].replace(" ", "")
        if time is None or time == "":
            time = "05:00PM"
        return self.datetime(time)


class MileIQ:
    """A MileIQ data structure"""

    def __init__(self, start_date, end_date, category, start, stop, miles,
                 miles_value=None, parking=None, tolls=None, total=None,
                 vehicle=None, purpose=None, notes=None):
        self.data = collections.OrderedDict()
        self.data["start_date"] = start_date
        self.data["end_date"] = end_date
        self.data["category"] = category
        self.data["start"] = start
        self.data["stop"] = stop
        self.data["miles"] = miles
        if miles_value:
            self.data["miles_value"] = miles_value
        if parking:
            self.data["parking"] = parking
        if tolls:
            self.data["tolls"] = tolls
        if total:
            self.data["total"] = total
        if vehicle:
            self.data["vehicle"] = vehicle
        if purpose:
            self.data["purpose"] = purpose
        if notes:
            self.data["notes"] = notes

    def to_csv(self):
        # wrap all the values in quotes because addresses contain commas
        return ''.join(['"', '","'.join(self.data.values()), '"'])


if __name__ == '__main__':

    try:
        if len(sys.argv) > 1:
            filename = sys.argv[1]
            f = open(filename, 'r')
        else:
            f = sys.stdin.read().splitlines()
        begin = False
        csv = csv.reader(f)
        for row in csv:
            if row:
                if row[0] == 'Deduction':
                    begin = True
                    print "START_DATE*,END_DATE*,CATEGORY*,START*,STOP*,MILES*,MILES_VALUE,PARKING,TOLLS,TOTAL,VEHICLE,PURPOSE,NOTES"
                    continue
                elif begin and re.match(r"\$\d+\.\d+$", row[0]):
                    everlance = Everlance(*row)
                    mileIQ = everlance.to_mileIQ()
                    print mileIQ.to_csv()

    except Exception, e:
        print "Error Reading from file"
        traceback.print_exc(file=sys.stdout)
    finally:
        if isinstance(f, file):
            f.close()
