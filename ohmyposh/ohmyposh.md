# Install OHMYPOSH

```bash
sudo wget https://github.com/JanDeDobbeleer/oh-my-posh/releases/latest/download/posh-linux-amd64 -O /usr/local/bin/oh-my-posh
sudo chmod +x /usr/local/bin/oh-my-posh
mkdir ~/.poshthemes
wget https://github.com/JanDeDobbeleer/oh-my-posh/releases/latest/download/themes.zip -O ~/.poshthemes/themes.zip
unzip ~/.poshthemes/themes.zip -d ~/.poshthemes
chmod u+rw ~/.poshthemes/*.json
rm ~/.poshthemes/themes.zip
```


## Add to the .bashrc

```
eval "$(oh-my-posh init bash)"
#related to theme
eval "$(oh-my-posh init bash --config ~/.poshthemes/powerlevel10k_rainbow.omp.json)"
```

## To install font follow this video

it will not work then need to install nerd font

folow this video

https://www.ceos3c.com/wsl-2/windows-terminal-customization-wsl2-deep-dive/#part-1-install-zsh-on-wsl2


## configure termninal fonts 

choose MesloLGS NF

## in VSCODE terminal

### in settings

terminal.integrated.fontFamily

choose MesloLGS NF

instruction

[https://github.com/romkatv/powerlevel10k/issues/671](https://github.com/romkatv/powerlevel10k/issues/671)




