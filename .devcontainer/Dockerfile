FROM mcr.microsoft.com/devcontainers/python:3.11-bullseye

# Install Node.js 20.x
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs

# Upgrade npm (now supported by Node 20.x)
ENV NPM_CONFIG_UNSAFE_PERM=true
RUN npm install -g npm@latest

# Install global Node.js tools
RUN npm install -g \
    typescript \
    next \
    eslint \
    prettier \
    nodemon \
    pm2

# Install additional development tools
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
        postgresql-client \
        redis-tools \
        vim \
        curl \
        wget \
        git \
        jq \
        tree \
        htop \
        make \
        build-essential \
        software-properties-common \
    && apt-get autoremove -y && apt-get clean -y

# Install Docker CLI
RUN curl -fsSL https://get.docker.com | sh

# Install Python development tools
RUN pip install --upgrade pip setuptools wheel

# Install global Python tools
RUN pip install \
    black \
    flake8 \
    isort \
    pylint \
    pytest \
    pytest-django \
    pre-commit \
    django-extensions \
    ipython

# Create workspace directory
WORKDIR /workspace

# Set up git safe directory
RUN git config --global --add safe.directory /workspace

# Set up shell aliases
RUN echo 'alias ll="ls -la"' >> /home/vscode/.bashrc \
    && echo 'alias la="ls -la"' >> /home/vscode/.bashrc \
    && echo 'alias ..="cd .."' >> /home/vscode/.bashrc \
    && echo 'alias ...="cd ../.."' >> /home/vscode/.bashrc \
    && echo 'export PATH="/workspace/backend/venv/bin:$PATH"' >> /home/vscode/.bashrc \
    && echo 'cd /workspace' >> /home/vscode/.bashrc

# Switch to vscode user
USER vscode
