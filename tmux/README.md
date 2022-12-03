# tmux

I have started to learn `tmux` as that is the only shell pane tool that is available for use for taking the Certified Kubernetes Administrator (CKA) exam. 

# Configuration

Add the following to `~/.tmux.conf` to change the default prefix from the awkward to reach `CTRL-B` to the closer `CTRL-A`:

```
unbind C-b
set -g prefix C-a
bind-key C-a send-prefix
```

To turn on changing panes and resizing by mouse

```
set -g mouse on
```

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

- Split a pane horizontally: `CTRL-A %`
- Split a pane vertically: `CTRL-A "`

## Navigation

- Navigate **up** a pane: `CTRL-A ↑`
- Navigate **down** a pane: `CTRL-A ↓`
- Navigate **left** a pane: `CTRL-A ←`
- Navigate **right** a pane: `CTRL-A →`

## Resizing a pane

- Resize current pane **up**: `CTRL-A Option-↑`
- Resize current pane **down**: `CTRL-A Option-↓`
- Resize current pane **left**: `CTRL-A Option-←`
- Resize current pane **right**: `CTRL-A Option-→`
