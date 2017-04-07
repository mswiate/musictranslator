# musictranslator
Translate some great poems to fantastic classical music!

## How to use

```shell
> python run.py -o output.mid
> python run.py -o output.mid --poem poems\Erlkonig.txt --lang German --rhythm dynamic  --scale MINOR --chords 1
```

```
usage: run.py [-h] [--lang LANG] [-o O] [--poem POEM] [--gama {1,2}]
              [--rhythm {cut,dynamic}] [--scale {MINOR,MAJOR}] [-l]
              [--chords {0,1,2,3,4,5,6,7,8}]

parse poems to melancholic, narcotic midi!

optional arguments:
  -h, --help            show this help message and exit
  --lang LANG           languages: English, French, German, Spanish,
                        Portuguese, Italian, Turkish, Swedish, Polish, Dutch,
                        Danish, Icelandic, Finnish, Czech
  -o O                  output file name
  --poem POEM           a file with your poem
  --gama {1,2}          how wide (in octaves) the gama should be?
  --rhythm {cut,dynamic}
                        if you prefer brainwashing music choose dynamic
  --scale {MINOR,MAJOR}
                        if happy choose minor, otherwise choose minor
  -l                    if pitch is to high
  --chords {0,1,2,3,4,5,6,7,8}
                        higher int sparser chords
```

## Requirements

 - Python 3.6
 - miditime 1.1.3
