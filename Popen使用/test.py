from os.path import isfile
from os import devnull
from subprocess import Popen
PIPE = -1
STDOUT = -2
DN = open(devnull, 'w')
def detect_camera():
    show_camera_cmd = Popen(['lsusb'], stdout = PIPE, stderr = DN)
    show_camera_cmd.wait()
    
    if not isfile('/dev/video0'):
        for line in show_camera_cmd.communicate()[0].split('\n'):
            list_1 = line.split()
            try:
                if str(list_1).find('Webcam') != -1:
                    return True
            except:
                pass
    return False

def main():
    print detect_camera()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print _('detect camer over.')