FROM python:3.7
WORKDIR /root/
ARG BRANCH="master"
ARG NUM_CORES=2

RUN echo "deb http://ftp.us.debian.org/debian unstable main contrib non-free" >> /etc/apt/sources.list.d/unstable.list &&\
    apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    cmake \
    libgmp-dev \
    libmpfr-dev \
    libgmpxx4ldbl \
    libboost-dev \
    libboost-thread-dev \
    zip unzip patchelf && \
    apt-get clean && \
    git clone --single-branch -b $BRANCH https://github.com/MarcusAndreasSvensson/PyMesh.git

ENV PYMESH_PATH /root/PyMesh
ENV NUM_CORES $NUM_CORES
WORKDIR $PYMESH_PATH

RUN git submodule update --init && \
    pip install -r $PYMESH_PATH/python/requirements.txt && \
    ./setup.py bdist_wheel && \
    rm -rf build third_party/build && \
    python $PYMESH_PATH/docker/patches/patch_wheel.py && \
    pip install dist/pymesh2*.whl && \
    python -c "import pymesh; pymesh.test()"

COPY src/Api/API.py API.py
COPY src/Api/create_calc_mesh.py create_calc_mesh.py
COPY src/Api/1591733049157_ABSKG-40AL9_VAZPF-008_132S_76NO_102332978.stl 1591733049157_ABSKG-40AL9_VAZPF-008_132S_76NO_102332978.stl
RUN pip install flask
RUN pip install flask-cors
RUN pip install requests
CMD [ "python3", "API.py" ]