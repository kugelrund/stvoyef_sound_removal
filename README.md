# stvoyef_sound_removal

By disabling audio output when speedrunning, Star Trek: Voyager - Elite Force
dialogs are completely skipped which saves a lot of time. However as it is
pretty anticlimactic to play without sounds, an alternative is to delete only
those specific sound files that influence progression of the game (see also
[the speedrun.com page](https://www.speedrun.com/stvoyef)). These scripts are
an attempt to automate the process of deleting these sound files from the
game's `.pk3` archives.

Python 3 is required to run these scripts.

## Removing Sounds

To remove the sounds from the game's `.pk3` files, run the `remove_sounds.py`
script. It takes the path to a text file with a list of sounds to remove as
first command line argument and the path to the `.pk3` files from which to
remove the sounds as second argument. So the simplest way is to put the script
`remove_sounds.py` together with a file `sounds_to_remove.txt` and the game's
`.pk3` files `pak0.pk3`, `pak1.pk3`, `pak2.pk3` and `pak3.pk3` next to each
other in one directory and run:

```bash
$ python3 remove_sounds.py sounds_to_remove.txt *.pk3
```

An appropriate `sounds_to_remove.txt` file can be downloaded from the
[Releases](https://github.com/kugelrund/stvoyef_sound_removal/releases).
To generate the file yourself, perhaps with customizations, see the
[next section](#find-sounds-to-remove).

## Find Sounds to Remove

To generate the text file with a list of sounds to remove you will need to
obtain the original `real_scripts` script files for
Star Trek: Voyager - Elite Force. Then, run

```bash
$ python3 find_sounds_to_remove.py path/to/real_scripts
```

which will generate the file `sounds_to_remove.txt` in the current working
directory.
