# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

from os import path
import subprocess

@hook.subscribe.startup_once
def autostart():
    subprocess.call([path.join(path.expanduser('~'),'.config','qtile','autostart.sh')])
def pulseaudio():
    subprocess.call([path.join(path.expanduser('~'),'.config','qtile','pulseaudio.sh')])

mod = "mod4"
terminal = guess_terminal()

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn("alacritty"), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    #scrot
    Key([mod], "s", lazy.spawn("scrot")),
     # Menu
    Key([mod], "m", lazy.spawn("rofi -show drun")),
    # Window Nav
    Key([mod, "shift"], "m", lazy.spawn("rofi -show"))
]

groups = [Group(i) for i in ["  ", "  ", "  ", "  " ,"  "]]

for i, group in enumerate(groups):
    actual_key = str(i + 1)
    keys.extend([
        # Switch to workspace N
        Key([mod], actual_key, lazy.group[group.name].toscreen()),
        # Send window to workspace N
        Key([mod, "shift"], actual_key, lazy.window.togroup(group.name))
    ])


layout_conf = {
    'border_focus':'#F07178',
    'border_width':1,
    'margin':4
}
    
layouts = [
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layout.Max(**layout_conf),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    layout.MonadTall(**layout_conf),
    layout.MonadWide(**layout_conf),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="UbuntuMono Nerd Font",
    fontsize=16,
    padding=3
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    foreground=["f1ffff","#f1ffff"],
                    background=["#0f101a","#0f101a"],
                    font='UbuntuMono Nerd Font',
                    fontsize=18,
                    margin_y=3,
                    margin_x=0,
                    padding_y=8,
                    padding_x=5,
                    borderwidth=1,
                    active=["#f1ffff","#f1ffff"],
                    inactive=["#f1ffff","#f1ffff"],
                    rounded=False,
                    highlight_method='block',
                    this_current_screen_border=["#F07178","#F07178"],
                    this_screen_border=["#5c5c5c","#5c5c5c"],
                    other_current_screen_border=["#0f101a","#0f101a"],
                    other_screen_border=["#0f101a","#0f101a"]
                ),
                widget.WindowName(
                    foreground=["f1ffff","#f1ffff"],
                    background=["#0f101a","#0f101a"],
                    fontsize=13,
                    font='UbuntuMono Nerd Font Bold'
                ),
                widget.Systray(
                    foreground=["#0f101a","#0f101a"],
                    background=["#0f101a","#0f101a"],
                    padding=5
                ),
                widget.TextBox(
                    foreground=["#0f101a","#0f101a"],
                    background=["#F3C97A","#F3C97A"], 
                    fontsize=16,
                    text='  '
                ),
                widget.CheckUpdates(
                    background=["#F3C97A","#F3C97A"], 
                    foreground=["f1ffff","#f1ffff"],
                    colour_have_updates=["#f1ffff","#f1ffff"],
                    colour_no_updates=["#f1ffff","#f1ffff"],
                    no_update_string='0',
                    display_format='{updates}',
                    update_interval=1800,
                    custom_command='checkupdates'
                ),
                widget.Sep(
                    background=["#F3C97A","#F3C97A"], 
                    linewidth=0, 
                    padding=5
                ),
                widget.Image(
                    filename=path.join(path.expanduser('~'), '.config', 'qtile','img', 'bar4.png')
                ),
                widget.Net(
                    interface='wlp3s0',
                    foreground=["#0f101a","#0f101a"],
                    background=["#ee977b","#ee977b"]
                ),
                widget.Image(
                    filename=path.join(path.expanduser('~'), '.config', 'qtile','img', 'bar3.png')
                ),
                widget.CurrentLayoutIcon(
                    foreground=["#0f101a","#0f101a"],
                    background=["#F07178","#F07178"],
                    scale=0.65
                ),
                widget.CurrentLayout(
                    foreground=["#0f101a","#0f101a"],
                    background=["#F07178","#F07178"]
                ),
                widget.Sep(
                    background=["#F07178","#F07178"],
                    linewidth=0, 
                    padding=5
                ),
                widget.Image(
                    filename=path.join(path.expanduser('~'), '.config', 'qtile','img', 'bar1.png')
                ),
                widget.TextBox(
                    background=["#a151d3","#a151d3"],
                    foreground=["#0f101a","#0f101a"],
                    text='  ' 
                ),
                widget.Clock(
                    background=["#a151d3","#a151d3"],
                    foreground=["#0f101a","#0f101a"],
                    format='%d/%m/%Y - %H:%M ')
            ],
            26,
            opacity=0.95
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    foreground=["f1ffff","#f1ffff"],
                    background=["#0f101a","#0f101a"],
                    font='UbuntuMono Nerd Font',
                    fontsize=18,
                    margin_y=3,
                    margin_x=0,
                    padding_y=8,
                    padding_x=5,
                    borderwidth=1,
                    active=["#f1ffff","#f1ffff"],
                    inactive=["#f1ffff","#f1ffff"],
                    rounded=False,
                    highlight_method='block',
                    this_current_screen_border=["#F07178","#F07178"],
                    this_screen_border=["#5c5c5c","#5c5c5c"],
                    other_current_screen_border=["#0f101a","#0f101a"],
                    other_screen_border=["#0f101a","#0f101a"]
                ),
                widget.WindowName(
                    foreground=["f1ffff","#f1ffff"],
                    background=["#0f101a","#0f101a"],
                    fontsize=13,
                    font='UbuntuMono Nerd Font Bold'
                ),
                widget.Sep(
                    background=["#0f101a","#0f101a"],
                    linewidth=0, 
                    padding=5
                ),
                widget.TextBox(
                    foreground=["#0f101a","#0f101a"],
                    background=["#F3C97A","#F3C97A"], 
                    fontsize=16,
                    text='  '
                ),
                widget.CheckUpdates(
                    background=["#F3C97A","#F3C97A"], 
                    foreground=["f1ffff","#f1ffff"],
                    colour_have_updates=["#f1ffff","#f1ffff"],
                    colour_no_updates=["#f1ffff","#f1ffff"],
                    no_update_string='0',
                    display_format='{updates}',
                    update_interval=1800,
                    custom_command='checkupdates'
                ),
                widget.Sep(
                    background=["#F3C97A","#F3C97A"], 
                    linewidth=0, 
                    padding=5
                ),
                widget.Image(
                    filename=path.join(path.expanduser('~'), '.config', 'qtile','img', 'bar4.png')
                ),
                widget.Net(
                    interface='wlp3s0',
                    foreground=["#0f101a","#0f101a"],
                    background=["#ee977b","#ee977b"]
                ),
                widget.Image(
                    filename=path.join(path.expanduser('~'), '.config', 'qtile','img', 'bar3.png')
                ),
                widget.CurrentLayoutIcon(
                    foreground=["#0f101a","#0f101a"],
                    background=["#F07178","#F07178"],
                    scale=0.65
                ),
                widget.CurrentLayout(
                    foreground=["#0f101a","#0f101a"],
                    background=["#F07178","#F07178"]
                ),
                widget.Sep(
                    background=["#F07178","#F07178"],
                    linewidth=0, 
                    padding=5
                ),
                widget.Image(
                    filename=path.join(path.expanduser('~'), '.config', 'qtile','img', 'bar1.png')
                ),
                widget.TextBox(
                    background=["#a151d3","#a151d3"],
                    foreground=["#0f101a","#0f101a"],
                    text='  ' 
                ),
                widget.Clock(
                    background=["#a151d3","#a151d3"],
                    foreground=["#0f101a","#0f101a"],
                    format='%d/%m/%Y - %H:%M ')
            ],
            26,
            opacity=0.95
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    )
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ],
    border_focus='#a151d3'
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
