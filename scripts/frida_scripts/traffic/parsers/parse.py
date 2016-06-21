import os
import sys



PARSERS = {}

def run_parsers(filepath, parsingsdir):
    filename = os.path.basename(filepath)
    print "parsing " + filepath
    for n, p in PARSERS.items():
        res_path = os.path.join(parsingsdir, filename)+n+p.EXT
        p.parse(filepath, res_path)


def parse(outputs_dir, parsings_dir):
    for root, dirs, files in os.walk(outputs_dir):
        for name in files:
            run_parsers(os.path.join(root, name), parsings_dir)

if __name__ == "__main__":
    parse(sys.argv[1], sys.argv[2])
