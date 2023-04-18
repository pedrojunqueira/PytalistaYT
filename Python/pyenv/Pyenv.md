# Install Pyenv in Linux

## update Linux

`sudo apt update`

`sudo apt upgrade`

## update and upgrade and install libraries dependencies

```bash
sudo apt install \
    build-essential \
    curl \
    libbz2-dev \
    libffi-dev \
    liblzma-dev \
    libncursesw5-dev \
    libreadline-dev \
    libsqlite3-dev \
    libssl-dev \
    libxml2-dev \
    libxmlsec1-dev \
    llvm \
    make \
    tk-dev \
    wget \
    xz-utils \
    zlib1g-dev
```

# install pyenv

`curl https://pyenv.run | bash`


## add to .bashrc file should look like this

```bash
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
if command -v pyenv 1>/dev/null 2>&1; then
  eval "$(pyenv init --path)"
  eval "$(pyenv init -)"
  eval "$(pyenv virtualenv-init -)"
fi
```


## basic usage of pyenv 

List available python versions to install

`pyenv install --list`

Install a version

`pyenv install 3.11.0`

Check Installed versions

`pyenv versions`

Make a version global (default)

`pyenv global 3.10.0`
