# aslicer

*automatic audio slicing through transient detection*

---

I've been using a DAW to do this manually for a while, thought I would save 
myself some time. This script should be able to process whatever filetypes `ffmpeg` 
supports, according to `pydub` documentation.

Install can be done by running `pipx install .`.

```bash
usage: python3 aslicer.py [options] sample1 sample2 ...
-h/--help		display this help message
-t/--threshold		set threshold for transient detection [default: 3.0]
-i/--keep-intro		keep audio before first detected transient [default: False]
-o/--output		write audio slices to directory argument (implies -d)
-d/--to-dir		write audio slices to directory named after file [default: False]

$ # slice multiple audio files to separate named directories
$ python3 aslicer.py -d audio1.wav audio2.mp3 audio3.flac
file: audio1.wav                    transients: 73
file: audio2.mp3                    transients: 73
file: audio3.flac                   transients: 73

$ # slice audio, detecting transients with a >5.0 change-in-rms ratio
$ python3 aslicer.py -t 5.0 audio.wav
file: audio.wav                     transients: 41

$ # slice audio to specific directory
$ python3 aslicer.py -o some/directory/path audio.wav
file: audio.wav                     transients: 73
```
