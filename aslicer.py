import getopt
import sys
import os
from pathlib import Path
from pydub import AudioSegment


def help(code: int = None):
    """
    Help message. Exit's with status `code` if not None.
    """
    print(
        f"usage: {sys.argv[0]} [options] sample1 sample2 ...", file=sys.stderr
    )
    print("-h/--help\t\tdisplay this help message")
    print(
        "-t/--threshold\t\tset threshold for transient detection [default: 3.0]",
        file=sys.stderr,
    )
    print(
        "-i/--keep-intro\t\tkeep audio before first detected transient [default: False]",
        file=sys.stderr,
    )
    print(
        "-o/--output\t\twrite audio slices to directory argument (implies -d)",
        file=sys.stderr,
    )
    print(
        "-d/--to-dir\t\twrite audio slices to directory named after file [default: False]",
        file=sys.stderr,
    )
    if code is not None:
        sys.exit(code)


def main():
    keep_intro = False
    output_format = "wav"
    output_directory = None
    threshold = 3.0

    opts, args = getopt.getopt(
        sys.argv[1:],
        "hit:o:d",
        ["help", "keep-intro", "threshold=", "output=", "to-dir"],
    )

    # Process options
    for o, a in opts:
        if o in ["-h", "--help"]:
            help(0)
        elif o in ["-i", "--keep-intro"]:
            keep_intro = True
        elif o in ["-t", "--threshold"]:
            try:
                threshold = float(a)
            except ValueError:
                raise Exception("threshold must be a valid float")
            if threshold <= 0:
                raise Exception("threshold value must be positive")
        elif o in ["-o", "--output"]:
            if os.path.exists(a) and (not os.path.isdir(a) or not os.access(a, os.W_OK)):
                raise Exception(f"cannot create output directory '{a}'")
            else:
                output_directory = a
        elif o in ["-d", "--to-dir"]:
            if not output_directory:
                output_directory = ""
        else:
            help(1)

    # Check arguments
    if len(args) == 0:
        help(1)

    files = []
    for a in args:
        p = Path(a)
        if not p.exists():
            raise Exception(f"file '{a}' does not exist")
        files.append((a, a[0 : -len(p.suffix)], p.suffix.strip(".")))

    for f in files:
        audio = AudioSegment.from_file(f[0], f[2])
        transients = []

        if keep_intro:
            transients.append(0)

        baseline = audio[0].rms
        a = 0.95
        maxDeriv = 0.01
        cooldown = 10
        cool = 0

        for i in range(1, len(audio)):
            # calculate baseline
            baseline = a * baseline + (1 - a) * audio[i].rms
            # update energy ratio
            ratio = audio[i].rms / (baseline + 1e-9)
            # derivative for calculating change
            deriv = audio[i].rms - audio[i - 1].rms

            if cool == 0:
                if ratio > threshold and deriv > maxDeriv:
                    transients.append(i)
                    cool = cooldown
                    print(
                        f"file: {f[0]:<30}transients: {len(transients)}",
                        end="\r",
                        file=sys.stderr,
                    )
            else:
                cool -= 1
        print("")
        if len(audio) - 1 not in transients:
            transients.append(len(audio) - 1)

        directory = f[1] if output_directory == "" else output_directory
        if directory and not os.path.exists(directory):
            os.mkdir(directory)

        for i in range(1, len(transients)):
            seg = audio[transients[i - 1] : transients[i]]
            seg.export(
                "{}{}_{}.{}".format(
                    (directory + "/" if directory else ""),
                    f[1],
                    i,
                    output_format,
                ),
                output_format,
            )


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"error: {e}")
        help(1)
