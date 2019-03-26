# ANTUR

![DAAD compiling CLOUD99 source generated with ANTUR.](http://f.cl.ly/items/2H2O2n1p2f1I2m2K1u3E/antur_cloud99.gif "DAAD compiling CLOUD99 source generated with ANTUR.")

ANTUR (Welsh for adventure) is a transcompiler, meant to assist 8-bit & 16-bit text/graphic adventure authors. It converts sources for Gilsoft's `PAWs` to sources ready to compile in Infinite Imagination's `DAAD Adventure Writer`.

## Scenarios

While PAWs is restricted to ZX Spectrum and CP/M, DAAD uses the same source to compile interactive fiction for `C64, ZX Spectrum, Amstrad CPC, MSX, Amiga, Atari ST and DOS (IBM-PC)`. You could develop your game with PAWs on Spectrum and then use ANTUR to target the other systems. You might also use inPAWs for development. Maybe you want to port your classic Spectrum adventure to Commodore 64? With ANTUR, you can.

## Prerequisites

Since ANTUR is a transcompiler, it transforms a PAWs source to a DAAD source. The input file needs to be a PAWs `.SCE file`, which is the PAWs for CP/M format. If your adventure was made in Spectrum PAWs, you may use `inPAWs` to easily convert the game from a Spectrum database to a CP/M source.

## Editor

When dealing with .SCE or .PAW files, I highly recommend using `VSCode`. We created syntax highlighters for [.SCE (PAWs and DAAD)](https://marketplace.visualstudio.com/items?itemName=ainslec.daad-paws-sce) as well as [.PAW (inPAWs)](https://marketplace.visualstudio.com/items?itemName=ainslec.inpaws).

## Input files

Make sure the file you're about to convert is okay, meaning it would definitely compile in CP/M PAWs and that it's following Gilsoft's conventions for said file type. ANTUR won't resolve any errors. Here is the structure of a proper .SCE source. The sections have to be in that order.

```python
/VOC # vocabulary
/STX # system messages
/MTX # message texts
/OTX # object texts
/LTX # location texts
/CON # connections
/OBJ # object definitions
/PRO # process tables
```

You don't have to worry much about whitespace or tabs in your input file, neither trailing nor elsewhere, but there is one rule you urgently need to follow: in a process table, the distance between a CondAct and its value needs to be a single whitespace. Here is an example of how a good input file would look like.

![Example of a good PAWs CP/M input file.](http://f.cl.ly/items/1j3B450i403A3h461I2S/antur_coding_style.png "Example of a good PAWs CP/M input file.")

Note that DAAD's Spectrum target can't handle 128k games. You may devide a larger story into two or three chapters.

## Transcompilation

Let's have a look what happens during ANTUR's transcompilation process:

* reformatting the content, removing unnecessary and trailing whitespace
* adding a standard set of tokens for text compression
* replacing `system message 10` with DAAD's standard message for this location
* replacing `system messages 54-62` with DAAD's standard messages for this location
* rearrangig object definitions and converting them to DAAD's syntax
* adding the standard set of process tables and commands necessary for DAAD to work
* adapting process 0 content to DAAD's command decoder, located at process 5
* adapting process 1 content to DAAD's process 3
* adapting process 2 content to DAAD's process 4
* relocating process `tables >2` (if existing) to process `tables >6`
* updating process table CondActs to the new locations
* replacing no longer implemented `INVEN` CondAct with DAAD's logic
* refactoring no longer implemented `TIMEOUT and PROMPT` CondActs to DAAD symbols
* refactoring `DESC, PARSE, SAVE, LOAD and RAMSAVE` CondActs to DAAD's format
* refactoring `TURNS and SCORE` CondActs to DAAD symbols
* other stuff I very likely have forgotten to mention here

## Output files

The generated output files are .SCE files as well, but DAAD's implementation, which is an evolution of the original format. DAAD's .SCE structure is similar but not the same, and it introduces several new sections such as tokens used for text compression, per-object attributes and generally a much advanced and expanded syntax for an even more sophisticated system. Since DAAD is multi-language, ANTUR supports both `English` and `Spanish` output files.

## Aftermath

ANTUR creates files that highly likely compile with `DC.EXE` (DAAD's compiler) out of the box. That doesn't mean though you won't need to touch the sources. Here are a few things you should definitely check after the compilation process:

* Does the inventory code still work? PAWs used an `INVEN` CondAct which is not existing in DAAD, so when found it gets replaced by a few lines of code taken from DAAD's standard file template.
* PAWs INVEN uses SYSMESS 11 for "nothing". DAAD, as we already learned, uses LISTAT in the place of INVEN. LISTAT uses SYSMESS 53 for the "nothing" response in both PAWs and DAAD. PAWs users may have customised this message for container-specific LISTAT routines, so authors may wish to check and alter the message if necessary.
* Object listings at locations: many PAWs adventures made use of the `LISTOBJ` CondAct for locations. ANTUR adds DAAD's equivalent of this at the beginning of `/PRO 3`. This could result in seeing the objects listed twice at locations if you keep the old implementation in. You may choose which one you keep but I suggest you go with DAAD's version as that makes use of the `DarkF` symbol, which is a pointer to the flag that defines whether a room is dark or not.
* System messages: ANTUR replaces system message 10 with DAAD's standard value "You are wearing", which might not be wanted. ANTUR also swaps system messages `54-62` with DAAD's standard messages at these locations. Since this block controls tape and disk operations, it's mandatory that said messages remain. System messages in PAWs were located between 0-60, so it could be that the conversion process made you loose a few messages. If so, you should manually add these again to end of the system message block and refactor the code that triggers those messages by hand.
* Since `SCORE and TURNS` CondActs are not available in DAAD, they get replaced with symbols pointing to DAAD's system flags for score and turns. This results in seeing just the bare integers on screen where you've read a fancy message in PAWs. You might want to work on this by adding new messages around those numbers to resemble the look and feel of PAWs.
* Flags: To avoid any conflicts resulting in odd behaviour or non working games, it's mandatory to exclusively use flags `between 64-255`. DAAD treads flags `0-63 system flags` and also defines symbolic names for these (see DAAD's symbols.sce file). Although DAAD does not reference all of those flags, it is possible they may be treated specially by future upgrades. Yes, it's not ruled out that Tim and I will do another DAAD update in the future. So avoid using 0-63 and refactor any flags in this range. A detailed description of the flags is found in the DAAD documentation. I've chosen against auto-relocating flags by ANTUR, as I think this process is better carried out by hand. You may also want to make use of DAAD's symbol feature, that links words to numbers. Below is an example taken from the sources of my adventure `Eight Feet Under` the addon for my acclaimed game [Hibernated](https://8bitgames.itch.io/hibernated1). You may create those symbols for objects or messages, too.

![Example how to use symbols for flags.](http://f.cl.ly/items/3f0x2y0l1z1L3b001n0S/flags_refactoring.png "Example how to use symbols for flags.")

## Installation

For now, just download the contents of this repository and put `antur.py` into a directory of desire. I will create a PyPI package at a later date. The current version `0.2.1` is considered stable.

## Usage

Make sure you have `Python 3` at your path. If you're not familiar with Python and you're struggling to decide which version to install, I can highly recommmend [Anaconda](https://www.anaconda.com/distribution/), which is my Python distribution of choice. On Linux, BSD and MacOS, it should be sufficient enough to start ANTUR with `./antur.py` and it will show you detailed usage information. On Windows systems, you likely need to start ANTUR with `python antur.py`.

## System availability and documentation

You are probably wondering where you get PAWs (if needed) or DAAD from. The latest versions are available on the pages referenced below. No worries, this is legal. I'm maintaining the content together with Tim Gilberts, the original author of these tools.

PAWs: [http://8-bit.info/the-gilsoft-adventure-systems](http://8-bit.info/the-gilsoft-adventure-systems/) | DAAD: [http://8-bit.info/infinite-imaginations-aventuras-ad](http://8-bit.info/infinite-imaginations-aventuras-ad/)

We also talked about inPAWs, which is available from here: [http://inpaws.speccy.org/queesEng.html](http://inpaws.speccy.org/queesEng.html)

## Responsibility

ANTUR transforms source to source. I assume that you are either the author or the owner of this source code you are transcompiling with it. Tools like inPAWs allow recreation of sources from already compiled PAWs games by extracting the game database contents. So you could feed ANTUR with code that is not your own, which I strongly encourage you to not do. Please keep in mind that abandonware doesn't mean you may do whatever you want with it. Even after 30 years, old adventure classics are still the intellectual property of someone. If you're planning to use ANTUR for porting one of the Spectrum classics to other systems, let's say the Commodore 64 or the Amiga, make sure you are allowed to do so. I can't be held responsible for what you do with ANTUR. Needless to say you can.

## Credits

From the bottom of my heart I'd like to thank [Tim Gilberts](https://twitter.com/timbucus) for all his ongoing support. Without him, none of this would have been ever possible. I would also like to express my gratitude to [John Wilson](https://twitter.com/rochbalrog), which you may still remember as the man behind Zenobi Software. John provided a massive set of CP/M PAWs test files when I started developing ANTUR, containing valuable sources of his legendary adventures. Without his contribution, I probably would still be out bug hunting in the year 2037. John, today's word is legendary.

## License

ANTUR is copyright (C) 2019 Stefan Vogt, Pond Soft. It is released under the BSD 2-Clause License. See the file `LICENSE` for details.