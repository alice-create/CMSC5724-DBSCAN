import json
from argparse import ArgumentParser
from scanner import Scanner
import re
import sys

CONFIG = "config.json"
DATA = '3spiral.txt'

def DataLoader(DATA):
    data = []
    with open(DATA, 'r') as file_obj:
        lines = file_obj.readlines()
        for id, line in enumerate(lines):
            pos = line.strip("\n")
            x, y = map(float, pos.split())
            point = {"id":id, "value":[x,y]}
            data.append(point)

    return data

def ConfigLoader(CONFIG):
    config = {}
    try:
        with open(CONFIG, 'r') as file_obj:
            config = json.load(file_obj)
    except:
        print("Error reading the configuration file.\
                    expected lines: param = value \n param = {eps, min_pts, dim}, \
                    value = {float, int, int}")
        sys.exit()
    return config

def arg_parser():

    parser = ArgumentParser(description="Simple example of a training script.")
    parser.add_argument('--i', type=str, default="3spiral.txt", help="A path for the input data.")
    parser.add_argument('--eps', type=float, default=2.5, help="The value of epsilon.")
    parser.add_argument("--min_pts", type=int, default=3, help="The value of the minimum points.")
    args = parser.parse_args()

    return args



def main():
    args = arg_parser()
    DATA = args.i
    data = DataLoader(DATA)
    config = ConfigLoader(CONFIG)
    config["eps"] = args.eps
    config["min_pts"] = args.min_pts
    scanner = Scanner(config)
    scanner.dbscan(data)
    scanner.export()


if __name__ == "__main__":
    main()

