import subprocess

from commons import BINARY_PATH


def spawn_recorder(room):
    spawn_command = \
        f"{BINARY_PATH}BililiveRecorder/BililiveRecorder.Cli/bin/Release/net6.0/BililiveRecorder.Cli " \
        f"portable " \
        f"-d 63 " \
        f"--webhook-url " \
        f'"http://127.0.0.1:10261/process_video" ' \
        f'--filename ' \
        '"{{ roomId }}/{{ \"now\" | format_date: \"yyyyMMdd\" }}/{{ roomId }}-{{ \"now\" | format_date: \"yyyyMMdd\" }}-{{ \"now\" | format_date: \"HHmmss\" }}-{{ \"now\" | format_date: \"fff\" }}.flv" '\
        f'/storage/ ' \
        f'{room} '
    print(f"spawn recorder for {room}: {spawn_command}")
    return subprocess.Popen(spawn_command, shell=True)


class RecorderManager:

    def __init__(self, rooms):
        self.recorder_dict: {int: subprocess.Popen} = {room: spawn_recorder(room) for room in rooms}

    def update_rooms(self, new_rooms, dry_run=False):
        current_rooms = set(self.recorder_dict.keys())
        new_rooms_set = set(new_rooms)
        to_del_rooms = current_rooms.difference(new_rooms_set)
        to_new_rooms = new_rooms_set.difference(current_rooms)
        if not dry_run:
            for room in to_new_rooms:
                self.recorder_dict[room] = spawn_recorder(room)
            for room in to_del_rooms:
                self.recorder_dict[room].terminate()
                self.recorder_dict[room].wait(timeout=10)
                del self.recorder_dict[room]
        return to_new_rooms, to_del_rooms


if __name__ == '__main__':
    import time
    BINARY_PATH = "../exes/"
    manager = RecorderManager([1])

    time.sleep(10)

    manager.update_rooms([3])
    time.sleep(10)

