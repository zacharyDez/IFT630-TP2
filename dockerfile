FROM ubuntu:latest

# initial setup of linux dependencies
RUN apt-get update \
    && apt-get install -y \
        git \ 
        wget 

# miniconda installation simplest to install pyopencl
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ./miniconda.sh \
        && chmod +x ./miniconda.sh \
        && ./miniconda.sh -b -p $HOME/miniconda \
        && export PATH=$HOME/miniconda/bin:$PATH


#  instalation of pyopencl
RUN /bin/bash -c "source $HOME/miniconda/bin/activate \
        && conda config --add channels conda-forge \
        && conda install -y \
            pocl \
            pyopencl \
            pytest"
