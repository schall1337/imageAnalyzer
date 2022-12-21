# Docker

From the repository root, build the docker image:

```bash
docker build -t schall/image_analyzer:git -f docker/Dockerfile .
```

Run it while mounting the host's MATLAB installation into the container (must not be read-only because we have to build the MATLAB python engine):

```bash
docker run -it --rm -v /usr/local/MATLAB/:/usr/local/MATLAB -v /path/to/input_dir:/input:ro -v /path/to/output_dir:/output schall/image_analyzer:git
```

Now navigate to `main/src`, run the script, and finally export the output:

```bash
cd main/src
python3 main.py /input/some.pdf
cp ../../output/bildanalyse_report.pdf /output/some_report.pdf
```
