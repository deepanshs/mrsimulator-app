
FROM python:3.7.3

RUN apt-get -y update
RUN apt-get install -y --fix-missing \
    build-essential \
    gcc \
    wget \
    git \
    zip \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*

RUN wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh \
    bash miniconda.sh -b -p $HOME/miniconda \
    export PATH="$HOME/miniconda/bin:$PATH" \
    hash -r \
    conda config --set always_yes yes --set changeps1 no \
    conda update -q conda \
    conda info -a \
    conda create -q -n test-env python=3.7.3 \
    source activate test-env \
    conda install -c anaconda --file conda-requirements.txt \
    pip install mrsimulator
