FROM quay.io/jupyter/pytorch-notebook:cuda12-latest

ENV DEBIAN_FRONTEND=noninteractive

RUN pip install --no-cache-dir \
    pandas \
    matplotlib \
    seaborn \
    scikit-learn \
    jupyterlab-git \
    psycopg2-binary \
    fastapi \
    uvicorn \
    python-multipart

USER jovyan

CMD ["start-notebook.py"]
