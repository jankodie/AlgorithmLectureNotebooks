# Slim Python image
FROM python:3.13-slim

# Add user jovyan for binder compatibility
ARG NB_USER=jovyan
ARG NB_UID=1000
ENV USER=${NB_USER}
ENV NB_UID=${NB_UID}
ENV HOME=/home/${NB_USER}

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}
    
    
# Copy the project files and give it to jovyan
COPY . ${HOME}
USER root
RUN chown -R ${NB_UID} ${HOME}

# Installation of curl - we don't have it in the slim image
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

USER ${NB_USER}
    
# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Make sure uv’s install dir is on PATH
ENV PATH="/home/jovyan/.local/bin:${PATH}"

# Make home folder is the current working directory
WORKDIR /home/jovyan/

# Restore python environment from uv.lock and pyproject.toml
RUN uv sync

# Register the .venv as kernel
RUN uv run python -m ipykernel install \ 
    --user \
    --name=statistics \
    --display-name="Algorithms"

# Set environment variables for Jupyter
ENV PATH="/home/jovyan/.venv/bin:${PATH}"

# Expose port 8888
EXPOSE 8888

# Run Jupyter with these arguments
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser"]