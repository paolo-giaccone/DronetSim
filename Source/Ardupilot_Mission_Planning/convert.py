import sys
import json
import logging
import argparse

from config import LATEST_VERSION, DEFAULT_FILE_NAME, TAKEOFF, WAYPOINT

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# Parses input arguments
def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert QGC .plan to .mavlink format")

    parser.add_argument(
        "filepath", type=str, help="Usage: python3 main.py </path/to/file/>")
    parser.add_argument(
        "--out", type=str, help="MAVlink filename", default=DEFAULT_FILE_NAME)
    parser.add_argument(
        "--version", type=str, help="MAVlink version", default=LATEST_VERSION)
    parser.add_argument(
        "--takeoff", type=str, help="Add takeoff at start of mavlink", default=False)

    return parser.parse_args()


"""
This class manages the .plan conversion by 
loading the .plan, initializing the mav object
and writing the formated mav object to a new file
"""
class Converter():
    def __init__(self, filepath, out, takeoff, version):
        self.filepath = filepath
        self.out = out
        self.takeoff = takeoff
        self.version = version
        self.plan = {}

    def main(self):
        self.verify_format()
        mav = Mav(self.plan, self.version, self.takeoff)
        self.write_to_disk(mav.file)

        print("Successfully converted {} to {}".format(self.filepath, self.out))

    def verify_format(self):
        """Verifies plan format"""
        # TODO: check if its a .plan, and that its not empty
        try:
            with open(self.filepath) as f:
                self.plan = json.load(f)
                f.close()
        except FileNotFoundError:
            logging.error("Can't open specified file")
        except:
            logging.error("Unexpected error")

    def write_to_disk(self, mav):
        """Write mavlink object to file"""
        try:
            with open(self.out, "w+") as f:
                for line in mav:
                    f.write(str(line))
                f.close()
        except:
            logging.exception(
                "Unexpected error, could not append MAVlink object to file")


"""
This class converts a JSON .plan file to a 
formated mavlink file
"""
class Mav():
    def __init__(self, plan, version, takeoff):
        self.plan = plan
        self.header = "QGC WPL {}".format(version)
        self.takeoff = takeoff

        self.mission_items = self.convert()
        self.file = self.format_items()

    def convert(self):
        """Convert plan to mavlink plaintext file format"""

        mav_items = []
        plan_items = self.plan["mission"]["items"]

        for i, item in enumerate(plan_items):
            print(i)
            if "TransectStyleComplexItem" not in item.keys():
                frame = item["frame"]
                command = item["command"]

                auto_continue = 1 if item["autoContinue"] else 0
                parameters = ["Nan" if i is None else "{:.6f}".format(
                    i) for i in item["params"]]

                mav_item = [i, 0, frame, command, *parameters, auto_continue]
                mav_items.append(mav_item)
            else:
                sub_item = item["TransectStyleComplexItem"]["Items"]

                for j, item in enumerate(sub_item):
                    auto_continue = 1 if item["autoContinue"] else 0
                    parameters = ["Nan" if i is None else "{:.6f}".format(
                        i) for i in item["params"]]

                    mav_item = [i, 0, frame, command, *parameters, auto_continue]
                    mav_items.append(mav_item)

            

        return self.set_current_wp(mav_items)

    def set_current_wp(self, mission_items):
        """Finds and sets current waypoint flag"""
        flag = 0
        for item in mission_items:
            if item[3] is TAKEOFF and flag == 0:
                item[1] = 1
                flag = 1
            
            if item[3] is WAYPOINT:
                return mission_items

        logging.warning("No WAYPOINT detected! GroundSDK Flightplans require WAYPOINT to run flightplans")

        return mission_items

    def format_items(self):
        mav_file = []
        mav_file.append(self.header)

        # Not sure if this is needed.
        # However, parrot drones need to takeoff
        # before other drone functions are activated
        if self.takeoff:
            self.takeoff = [0, 1, 3, TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 0]
            mav_file.append("\n")
            mav_file.append(self.insert_tabs(self.takeoff))

        for line in self.mission_items:
            mav_file.append("\n")
            mav_file.append(self.insert_tabs(line))

        return mav_file

    def insert_tabs(self, target):
        """Insert tab between every item in target"""

        return"\t\t".join(str(t) for t in target)


if __name__ == "__main__":
    args = parse_args()

    converter = Converter(args.filepath, args.out, args.takeoff, args.version)
    converter.main()
