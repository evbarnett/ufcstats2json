### Usage

To read all stats:

`python ufcstats2json.py -o "<output directory>"`

If `-o` is unspecified, the default directory is `"."`

To read all new stats, starting from a previous run that completed:

`python ufcstats2json.py -u -o "<previous output directory>"`

Misc flags:

`-d` Print debug logs

### JSON File Structure