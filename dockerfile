FROM ubuntu:latest

# initial setup of linux dependencies
RUN apt-get update \
    && apt-get install --reinstall -y binutils \
    && apt-get install -y \
        git \ 
        wget \
        --reinstall binutils \
        build-essential

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

# installation of opencl
RUN apt install -y ocl-icd-opencl-dev \
        opencl-headers


# activate environment with:
        # source $HOME/miniconda/bin/activate