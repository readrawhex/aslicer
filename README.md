# aslicer

*automatic audio slicing through transient detection*

---

I've been using a DAW to do this manually for loading samples
into samplers for way, way too long.

According to [`pydub`](https://github.com/jiaaro/pydub), this script 
should support processing:

> ...a WAV file
> ...or a mp3
> ... or an ogg, or flv, or anything else ffmpeg supports.

since it loads the file using whatever extension is present in its pathname.

## usage

```bash
$ python3 aslicer.py -h
usage: python3 aslicer.py [options] sample1 sample2 ...
-h/--help		display this help message
-t/--threshold		set threshold for transient detection [default: 3.0]
-i/--keep-intro		keep audio before first detected transient [default: False]
-o/--output		write audio slices to directory argument (implies -d)
-d/--to-dir		write audio slices to directory named after file [default: False]
$
$ # slice multiple audio files to separate named directories
$ python3 aslicer.py -d audio1.wav audio2.mp3 audio3.flac
$ # slice audio, detecting transients with a >5.0 change-in-rms ratio
$ python3 aslicer.py -t 5.0 audio.wav
$ # slice audio to specific directory
$ python3 aslicer.py -o some/directory/path audio.wav
```
