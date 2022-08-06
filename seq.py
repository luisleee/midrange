import mido
from sys import argv


def to_range(filename):
    mid = mido.MidiFile(filename)
    tempo = 500000
    tpb = mid.ticks_per_beat

    res = []
    res2 = []
    set_tempo = get_set_tempo(mid)
    for track in mid.tracks:
        tempo_changes = set_tempo
        t = 0
        note = [None] * 128
        arr = []
        arr2 = []

        for msg in track:
            while len(tempo_changes) > 0:
                if tempo_changes[-1][0] <= t:
                    tempo = tempo_changes.pop()[1]
                else:
                    break
            if msg.is_meta:
                continue
            t += mido.tick2second(msg.time, tpb, tempo)
            if msg.type == "note_on":
                note[msg.note] = t
                try:
                    arr2.append(round(t * 1000))
                except:
                    pass
            if msg.type == "note_off":
                try:
                    arr.append([round(note[msg.note], 2), round(t, 2)])
                except:
                    pass
                note[msg.note] = None
        if len(arr) != 0:
            res.append(arr)
        if len(arr) != 0:
            res2.append(arr2)
    return (res, res2)


def get_set_tempo(midiFile):
    arr = []
    for track in midiFile.tracks:
        tick = 0
        for msg in track:
            if msg.type == "set_tempo":
                arr.append((tick, msg.tempo))
                continue
            tick += msg.time
    arr.sort(key=lambda x: -x[0])
    return arr

if __name__ == "__main__":
    if len(argv) <= 1:
        print("Usage: python3 index.py <input_file>")
        exit(0)

    filename = argv[1]
    arr, arr2 = to_range(filename)
    print(arr)
    print(arr2)
