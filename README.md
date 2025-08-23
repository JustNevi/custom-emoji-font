# Custom Emoji Font

This project simplifies the process of creating your own emoji font.

It provides a script that conveniently renames your images into the correct hex-based filename format. The actual font creation is handled by the [nanoemoji](https://github.com/googlefonts/nanoemoji/) library.

## Dependencies

- [nanoemoji](https://github.com/googlefonts/nanoemoji/)

All required libraries are listed in the `requirements.txt` file.

## Usage

### Unicode Ranges

You can specify the Unicode characters or ranges that will be used for your font.

**Pattern:**

```
# Ranges
0021-007E
# Single values
00B6
```

**Example:**

```
10FFF0-10FFF4
10FFF6
10FFF8
10FFF9-10FFFC
10FFFF
```

This example corresponds to the following list of codepoints:

`['10fff0', '10fff1', '10fff2', '10fff3', '10fff4', '10fff6', '10fff8', '10fff9', '10fffa', '10fffb', '10fffc', '10ffff']`

### Rename Images

Navigate to the `src` directory:

```bash
cd src
```

Run the script:

```bash
python main.py
```

### Build the Font

Use `nanoemoji` to build the final `.ttf` file:

```bash
nanoemoji --color_format glyf_colr_1 --family MyEmojiFamily $(find ../local/svgs/ -name '*.svg')
```

or:

```bash
nanoemoji --color_format glyf_colr_1 --family MyEmojiFamily ../local/svgs/*.svg
```

**Options explained:**

- `--color_format glyf_colr_1`: specifies glyph reuse (COLR v1 format) used by `nanoemoji`
- `--family MyEmojiFamily`: sets the font family name
- `$(find ../local/svgs/ -name '*.svg')`: expands to a list of SVG files
  e.g. `../local/svgs/10fff0.svg ../local/svgs/10fff1.svg ../local/svgs/10fff2.svg ...`

The generated font will be located in the `build/` directory.

## Tools

### Unicode Lookup

To look up Unicode codepoints, you can use:
[https://unicodes.jessetane.com/](https://unicodes.jessetane.com/)

### PNG to SVG Conversion

To convert PNG images to SVG, you can use the open-source tool:
[https://www.visioncortex.org/vtracer/](https://www.visioncortex.org/vtracer/)
