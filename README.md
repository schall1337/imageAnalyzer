# imageAnalyzer
Analyzes quality of images in pdf's


# requirements
- python (from Python 3.7)
- matlab (from R2019b)
- poppler pdfimages (0.68.0)

- exif==1.3.5
- fitz==0.0.1.dev2
- haishoku==1.1.8
- layoutparser==0.3.4
- matlab==0.1
- numpy==1.23.2
- opencv_python==4.6.0.66
- Pillow==9.3.0
- protobuf==4.21.12
- pyenchant==3.2.2
- PyMuPDF==1.20.2
- pytesseract==0.3.10
- reportlab==3.6.11
- wcag_contrast_ratio==0.9

# install (Windows 10)
Tested Windows 10, Python 3.10 and Matlab R2022b

## dictionary

files 'de_DE_frami.aff' and 'de_DE_frami.dic' [source](https://github.com/LibreOffice/dictionaries/tree/master/de) need to be moved to pyenchant folder
[...]\enchant\data\mingw64\share\enchant\hunspell

# run

To analyse PDF run main.py file with path of pdf file as parameter

example: python main.py myTestPdf.pdf

# install (Docker)
Tested with Linux, Python 3.7 and Matlab R2019b

## build docker image

From the repository root, build the docker image:

```bash
docker build -t schall/image_analyzer:git -f docker/Dockerfile .
```

## run

Run it while mounting the host's MATLAB installation into the container (must not be read-only because we have to build the MATLAB python engine):

```bash
docker run -it --rm -v /usr/local/MATLAB/:/usr/local/MATLAB -v /path/to/input_dir:/input:ro -v /path/to/output_dir:/output schall/image_analyzer:git
```

Now navigate to `main/src`, run the main.py with path of pdf file as parameter , and finally export the output:

```bash
cd main/src
python3 main.py /input/some.pdf
cp ../../output/bildanalyse_report.pdf /output/some_report.pdf
```
