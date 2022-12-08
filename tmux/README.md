# tmux

I have started to learn `tmux` as that is the only shell pane tool that is available for use for taking the Certified Kubernetes Administrator (CKA) exam. 

# Configuration

Add the following to `~/.tmux.conf` to change the default prefix. I use `CTRL-p` instead of the awkward to reach with one hand `CTRL-b`:

```
unbind C-b
set -g prefix C-p
bind-key C-p send-prefix
```

To turn on changing panes and resizing by mouse

```
set -g mouse on
```

This doesnt seem to work too well in iTerm2 on the Mac.

# Commands

Start tmux:

```sh
tmux
```

To start up a new session where the top pane is big and there are two smaller panes for reporting via something like `watch`.

```sh
#!/bin/sh 
tmux new-session -s "k8s" -d
tmux split-window -v
tmux resize-pane -D 10
tmux split-window -h
tmux -2 attach-session -d 
```

## Splitting panes

- Split a pane horizontally: `CTRL-p %`
- Split a pane vertically: `CTRL-p "`

## Navigation

- Navigate **up** a pane: `CTRL-p ↑`
- Navigate **down** a pane: `CTRL-p ↓`
- Navigate **left** a pane: `CTRL-p ←`
- Navigate **right** a pane: `CTRL-p →`

## Resizing a pane

- Resize current pane **up**: `CTRL-p Option-↑`
- Resize current pane **down**: `CTRL-p Option-↓`
- Resize current pane **left**: `CTRL-p Option-←`
- Resize current pane **right**: `CTRL-p Option-→`
