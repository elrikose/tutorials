# Homebrew (brew)

Website: https://brew.sh
Documentation: https://docs.brew.sh

Homebrew is built on top of Git and Ruby. There are a lot of Ruby-isms here.

- Formula - Package
- Bottles - Binary packages
- Cask - lets you install Mac apps
- Keg - Installed in /usr/local/Cellar
- Tap - Third-party repos, do git pull when you do a `brew update`

Get the brew configuration:

```
$ brew config
HOMEBREW_VERSION: 3.0.1
ORIGIN: https://github.com/Homebrew/brew
HEAD: c951be8d3c7b339c7e759b7c40aec859e09a70a5
Last commit: 5 days ago
Core tap ORIGIN: https://github.com/Homebrew/homebrew-core
Core tap HEAD: 01b065c9d89aa24b3109f5b44a22a8e6aceda6c3
Core tap last commit: 26 hours ago
Core tap branch: master
HOMEBREW_PREFIX: /usr/local
HOMEBREW_CASK_OPTS: []
HOMEBREW_EDITOR: vi
HOMEBREW_MAKE_JOBS: 4
Homebrew Ruby: 2.6.3 => /System/Library/Frameworks/Ruby.framework/Versions/2.6/usr/bin/ruby
CPU: quad-core 64-bit skylake
Clang: 12.0 build 1200
Git: 2.27.0 => /usr/local/bin/git
Curl: 7.64.1 => /usr/bin/curl
macOS: 11.1-x86_64
CLT: 12.4.0.0.1.1610135815
Xcode: N/A
```

List all of the kegs in the Cellar

```
$ brew ls dos2unix
/usr/local/Cellar/dos2unix/7.4.0/bin/dos2unix
/usr/local/Cellar/dos2unix/7.4.0/bin/mac2unix
/usr/local/Cellar/dos2unix/7.4.0/bin/unix2dos
/usr/local/Cellar/dos2unix/7.4.0/bin/unix2mac
/usr/local/Cellar/dos2unix/7.4.0/share/doc/ (9 files)
/usr/local/Cellar/dos2unix/7.4.0/share/man/ (4 files)
```

```
$ brew upgrade minikube
Warning: Treating minikube as a formula.
==> Upgrading 1 outdated package:
minikube 1.5.2 -> 1.17.1
==> Upgrading minikube 1.5.2 -> 1.17.1
==> Downloading https://homebrew.bintray.com/bottles/minikube-1.17.1.big_sur.bottle.tar.gz
==> Downloading from https://d29vzk4ow07wi7.cloudfront.net/645cc05655411bddc944818278eca867049e7e2712411dd7902
######################################################################## 100.0%
==> Pouring minikube-1.17.1.big_sur.bottle.tar.gz
==> minikube cask is installed, skipping link.
==> Caveats
zsh completions have been installed to:
  /usr/local/share/zsh/site-functions
==> Summary
🍺  /usr/local/Cellar/minikube/1.17.1: 8 files, 64.4MB
Removing: /usr/local/Cellar/minikube/1.5.2... (8 files, 51.5MB)
```
