# Random Crazy GIF Generator that Displays on Terminal

A Python script that generates random shapes, including cubes, tesseracts, and polygons, and displays them in an animated format on the terminal using ASCII art. It also supports generating a GIF for the random shapes.

## Installation

Before running the script, you'll need to install the required dependencies:

- **numpy**
- **pillow**
- **chafa.py**

To install these dependencies, you can run:

```bash
pip install numpy pillow chafa.py
```

You will also need **`uv`** to run the script. Follow the installation steps below:

### Install `uv` (Terminal Display Tool)

Install `uv` via our standalone installers:

- **On macOS and Linux:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

- **On Windows:**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Alternatively, you can install it via PyPI:

```bash
pip install uv
```

Or with `pipx`:

```bash
pipx install uv
```

## Usage

To run the script and generate a random GIF, use the following command:

```bash
python random_gif.py [-h] [-o OUTPUT] [-S SIZE] [-f FRAMES] [-d DURATION] [-s SPEED]
```

### Options:
- `-h`, `--help`: Show help message and exit.
- `-o`, `--output OUTPUT`: Specify the output filename for the GIF (e.g., `'output.gif'`).
- `-S`, `--size SIZE`: Set the size of the generated images. The default is `50` (minimum size is 50).
- `-f`, `--frames FRAMES`: Set the number of frames in the GIF. Default is `5`.
- `-d`, `--duration DURATION`: Set the duration of each frame in milliseconds. Default is `100`.
- `-s`, `--speed SPEED`: Adjust the speed factor for the frame duration. A value of `1.0` corresponds to normal speed, greater than `1` for faster, and less than `1` for slower.

### Example:
```bash
python random_gif.py -o out.gif -S 80 -f 20 -d 100 -s 1.0
```

This will generate a random shape GIF with 20 frames, each lasting 100 milliseconds, and save it as `out.gif`.

If you don’t specify an output file, the script will display the animation in the terminal.

## Example of Terminal Output:

```
<< Random Animated Shapes displayed in the terminal >>
```

Enjoy watching the random shapes like cubes, tesseracts, and polygons!

## License

This project is licensed under the MIT License.
