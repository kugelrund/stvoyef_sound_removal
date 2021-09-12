import argparse
import glob
import os
import subprocess


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('remove_list', type=str,
                        help="Path to file that lists sounds to remove.")
    parser.add_argument('paks', type=str, help="paks to modify.")
    args = parser.parse_args()

    with open(args.remove_list, 'r') as f:
        sounds_to_remove = f.read().splitlines()
    print(sounds_to_remove)

    # replace extension with wildcard because the game for example reads a .wav
    # even if .mp3 was given by mistake
    sounds_to_remove = [os.path.splitext(sound)[0] + '.*' for sound in sounds_to_remove]

    for pak in glob.glob(args.paks):
        # shells might be limited in number of arguments so lets do it in chunks
        for sounds_chunk in chunks(sounds_to_remove, 100):
            cmd = ['zip', '-d', pak] + sounds_chunk
            subprocess.run(cmd)


if __name__ == "__main__":
    main()
