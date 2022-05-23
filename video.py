import subprocess


def video_concate(video1, video2, videoout, cwd):
    """concates video using ffmpeg, adds .avi to given filenames"""
    f1 = video1
    f2 = video2
    f3 = videoout
    subprocess.call(
        'ffmpeg -i concat:"%s|%s" -codec copy %s' % (f1, f2, f3), shell=True, cwd=cwd
    )
    # subprocess.call('ffmpeg -i concat:"%s.avi|%s.avi" -codec copy %s_nc.avi' %('29820','29847','out'),shell = True)


def video_trim(videoin, videoout, start, duration, cwd):
    """trims vido.avi from start to end"""
    subprocess.call(
        "ffmpeg -i %s -ss %f -c copy -t %f %s" % (videoin, start, duration, videoout),
        shell=True,
        cwd=cwd,
    )


def images2video(fname, frate, cwd, out="out.mp4", **kws):
    """Images to video
    rotate 180:
    ffmpeg -i out.mp4 -vf "transpose=2,transpose=2" out1.mp4
    https://stackoverflow.com/questions/3937387/rotating-videos-with-ffmpeg
    """
    start_number = kws.get("sn", 1)
    rot = kws.get("rot", "0")
    rotate = {
        "0": "",
        "90ccv": ' -vf "transpose=0"',  # conter clockwise and vertical flip
        "90c": ' -vf "transpose=1"',  # clocwise
        "90cc": ' -vf "transpose=2"',  # conter clockwise
        "90cvf": ' -vf "transpose=3"',  # conter clockwise and vertical flip
        "180": ' -vf "transpose=2,transpose=2"',
    }
    txt = f"ffmpeg -framerate {frate} -start_number {start_number} -i {fname} {rotate[rot]} -r 30 -c:v libx264 -crf 18  {out}"
    print(txt)
    subprocess.call(txt, shell=True, cwd=cwd)


def video2ppt(vinput, cwd, out="forppt.mp4"):
    """Video to PowerPoint compatible"""
    txt = """ffmpeg -i {} -c:v libx264 -preset slow  -profile:v high -level:v 4.0 -pix_fmt yuv420p -crf 22 -codec:a aac-vf -vf "scale='bitand(oh*dar, 65534)':'bitand(ih/2, 65534)', setsar=1" {}""".format(
        vinput, out
    )
    result = subprocess.call(txt, shell=True, cwd=cwd)


def main():
    pass


if "__name__" == "__main__":
    main()
