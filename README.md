# stvoyef_sound_removal

## Removing Sounds

To remove the sounds from the game's `.pak` files, run the `remove_sounds.py`
script. It takes the path to a text file with a list of sounds to remove as
first command line argument and the path to the `.pak` files from which to
remove the sounds as second argument. So the simplest way is to put the script
`remove_sounds.py` together with a file `sounds_to_remove.txt` and the game's
`.pak` files `pak0.pak`, `pak1.pak`, `pak2.pak` and `pak3.pak` next to each
other in one directory and run:

```bash
$ python3 remove_sounds.py sounds_to_remove.txt *.pak
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
