import getopt
import sys
from pathlib import Path
from pydub import AudioSegment


def help(code : int = None):
    """
    Help message. Exit's with status `code` if not None.
    """
    print("usage: python3 aslice.py [options] sample1 sample2 ...\n")
    print("-h/--help\t\tdisplay this help message")
    print("-i/--keep-intro\tkeep audio before first detected transient")
    if code is not None:
        sys.exit(code)


def main():
    keep_intro = False
    output_format = "wav"

    opts, args = getopt.getopt(
        sys.argv[1:],
        "h",
        ["help"],
    )

    # Process options
    for o, a in opts:
        if o in ["-h", "--help"]:
            help(0)
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
        files.append((a, a[0:-len(p.suffix)], p.suffix.strip(".")))

    for f in files:
        audio = AudioSegment.from_file(f[0], f[2])
        transients = []

        if keep_intro:
            transients.append(0)

        baseline = audio[0].rms
        a = 0.95
        maxRatio = 2.0
        maxDeriv = 0.01
        cooldown = 10
        cool = 0

        for i in range(1, len(audio)):
            # calculate baseline
            baseline = a * baseline + (1 - a) * audio[i].rms
            # update energy ratio
            ratio = audio[i].rms / (baseline + 1e-9)
            # derivative for calculating change
            deriv = audio[i].rms - audio[i-1].rms

            if cool == 0:
                if ratio > maxRatio and deriv > maxDeriv:
                    transients.append(i)
                    cool = cooldown
                    print(f"index: {i},", audio[i].rms, ratio)
            else:
                cool -= 1
        if len(audio) - 1 not in transients:
            transients.append(len(audio) - 1)

        for i in range(1, len(transients)):
            seg = audio[i-1:i]
            print(
                "{}_{}.{}".format(
                    f[1],
                    i,
                    output_format
                )
            )
            seg.export(
                "{}_{}.{}".format(
                    f[1],
                    i,
                    output_format
                ),
                output_format,
            )
             

if __name__ == "__main__":
    main()
