# DotfilesArchive
Personal dotfiles archive
个人点文件档案

仅个人使用，开放以提供参考

/data:      dotfiles that keep origin location style
/script:    py pg to sync and backup dotfiles automatically

sync.py:
``` bash
# ## manual of sync.py
# python sync.py --dotfiles-refer [.yaml:to sign files that need to backup] --dotfiles-source [/:location of backup files]
```


```bash
# python sync.py --dotfiles-refer script/dotfile_refer.yaml --dotfiles-source data
```

