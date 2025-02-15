# ============================================================
# Authors: Brad Heffernan - Erik Dubois - Cameron Percival
# ============================================================
# pylint:disable=C0103,C0116,C0411,C0413,I1101,R1705,W0621,W0611,W0622
import gi

# from yaml import DirectiveToken

gi.require_version("Gtk", "3.0")

from os import rmdir, unlink, walk, execl, getpid, system, stat, readlink
from os import path, getlogin, mkdir, makedirs, listdir
from distro import id
import os
from gi.repository import GLib, Gtk
import sys
import threading
import shutil
import psutil
import datetime
import subprocess


# =====================================================
#              BEGIN DECLARATION OF VARIABLES
# =====================================================

distr = id()

sudo_username = getlogin()
home = "/home/" + str(sudo_username)

gpg_conf = "/etc/pacman.d/gnupg/gpg.conf"
gpg_conf_local = home + "/.gnupg/gpg.conf"

gpg_conf_original = "/usr/share/archlinux-tweak-tool/data/any/gpg.conf"
gpg_conf_local_original = "/usr/share/archlinux-tweak-tool/data/any/gpg.conf"

# login managers

# sddm
sddm_default_d1 = "/etc/sddm.conf"
sddm_default_d1_bak = "/etc/bak.sddm.conf"
sddm_default_d2 = "/etc/sddm.conf.d/kde_settings.conf"
sddm_default_d2_bak = "/etc/bak.kde_settings.conf"
sddm_default_d2_dir = "/etc/sddm.conf.d/"
sddm_default_d1_arco = "/usr/share/archlinux-tweak-tool/data/arco/sddm/sddm.conf"
sddm_default_d2_arco = (
    "/usr/share/archlinux-tweak-tool/data/arco/sddm.conf.d/kde_settings.conf"
)
# lightdm
lightdm_conf = "/etc/lightdm/lightdm.conf"
lightdm_conf_bak = "/etc/bak.lightdm.conf"
lightdm_greeter = "/etc/lightdm/lightdm-gtk-greeter.conf"
lightdm_greeter_bak = "/etc/bak.lightdm-gtk-greeter.conf"
lightdm_slick_greeter = "/etc/lightdm/slick-greeter.conf"
lightdm_slick_greeter_bak = "/etc/bak.slick-greeter.conf"
lightdm_conf_arco = "/usr/share/archlinux-tweak-tool/data/arco/lightdm/lightdm.conf"
lightdm_greeter_arco = (
    "/usr/share/archlinux-tweak-tool/data/arco/lightdm/lightdm-gtk-greeter.conf"
)
lightdm_greeter_arco_att = (
    "/usr/share/archlinux-tweak-tool/data/arco/lightdm/lightdm-gtk-greeter-att.conf"
)
ligthdm_slick_greeter_arco = (
    "/usr/share/archlinux-tweak-tool/data/arco/lightdm/slick-greeter.conf"
)
# lxdm
lxdm_conf = "/etc/lxdm/lxdm.conf"
lxdm_conf_bak = "/etc/bak.lxdm.conf"
lxdm_conf_arco = "/usr/share/archlinux-tweak-tool/data/arco/lxdm/lxdm.conf"

icons_default = "/usr/share/icons/default/index.theme"

samba_config = "/etc/samba/smb.conf"

mirrorlist = "/etc/pacman.d/mirrorlist"
arcolinux_mirrorlist = "/etc/pacman.d/arcolinux-mirrorlist"
xerolinux_mirrorlist = "/etc/pacman.d/xerolinux-mirrorlist"
arcolinux_mirrorlist_original = (
    "/usr/share/archlinux-tweak-tool/data/arco/arcolinux-mirrorlist"
)
pacman = "/etc/pacman.conf"
pacman_arch = "/usr/share/archlinux-tweak-tool/data/arch/pacman/pacman.conf"
pacman_arco = "/usr/share/archlinux-tweak-tool/data/arco/pacman/pacman.conf"
pacman_eos = "/usr/share/archlinux-tweak-tool/data/eos/pacman/pacman.conf"
pacman_garuda = "/usr/share/archlinux-tweak-tool/data/garuda/pacman/pacman.conf"
blank_pacman_arch = "/usr/share/archlinux-tweak-tool/data/arch/pacman/blank/pacman.conf"
blank_pacman_arco = "/usr/share/archlinux-tweak-tool/data/arco/pacman/blank/pacman.conf"
blank_pacman_eos = "/usr/share/archlinux-tweak-tool/data/eos/pacman/blank/pacman.conf"
blank_pacman_garuda = (
    "/usr/share/archlinux-tweak-tool/data/garuda/pacman/blank/pacman.conf"
)
neofetch_arco = "/usr/share/archlinux-tweak-tool/data/arco/neofetch/config.conf"
alacritty_arco = "/usr/share/archlinux-tweak-tool/data/arco/alacritty/alacritty.yml"

oblogout_conf = "/etc/oblogout.conf"
gtk3_settings = home + "/.config/gtk-3.0/settings.ini"
gtk2_settings = home + "/.gtkrc-2.0"
grub_theme_conf = "/boot/grub/themes/Vimix/theme.txt"
grub_default_grub = "/etc/default/grub"
xfce_config = home + "/.config/xfce4/xfconf/xfce-perchannel-xml/xsettings.xml"
xfce4_terminal_config = home + "/.config/xfce4/terminal/terminalrc"
alacritty_config = home + "/.config/alacritty/alacritty.yml"
alacritty_config_dir = home + "/.config/alacritty"
slimlock_conf = "/etc/slim.conf"
termite_config = home + "/.config/termite/config"
neofetch_config = home + "/.config/neofetch/config.conf"
nsswitch_config = "/etc/nsswitch.conf"
bd = ".att_backups"
config = home + "/.config/archlinux-tweak-tool/settings.ini"
config_dir = home + "/.config/archlinux-tweak-tool/"
polybar = home + "/.config/polybar/"
desktop = ""
autostart = home + "/.config/autostart/"
login_backgrounds = "/usr/share/backgrounds/archlinux-login-backgrounds/"
pulse_default = "/etc/pulse/default.pa"
bash_config = ""
zsh_config = ""
fish_config = ""

if path.isfile(home + "/.config/fish/config.fish"):
    fish_config = home + "/.config/fish/config.fish"
if path.isfile(home + "/.zshrc"):
    zsh_config = home + "/.zshrc"
if path.isfile(home + "/.bashrc"):
    bash_config = home + "/.bashrc"

bashrc_arco = "/usr/share/archlinux-tweak-tool/data/arco/.bashrc"
zshrc_arco = "/usr/share/archlinux-tweak-tool/data/arco/.zshrc"
fish_arco = "/usr/share/archlinux-tweak-tool/data/arco/config.fish"
account_list = ["Standard", "Administrator"]
i3wm_config = home + "/.config/i3/config"
awesome_config = home + "/.config/awesome/rc.lua"
qtile_config = home + "/.config/qtile/config.py"
qtile_config_theme = home + "/.config/qtile/themes/arcolinux-default.theme"
leftwm_config = home + "/.config/leftwm/config.ron"
leftwm_config_theme = home + "/.config/leftwm/themes/"
leftwm_config_theme_current = home + "/.config/leftwm/themes/current"

seedhostmirror = "Server = https://ant.seedhost.eu/arcolinux/$repo/$arch"
aarnetmirror = "Server = https://mirror.aarnet.edu.au/pub/arcolinux/$repo/$arch"

atestrepo = "[arcolinux_repo_testing]\n\
SigLevel = Optional TrustedOnly\n\
Include = /etc/pacman.d/arcolinux-mirrorlist"

atestrepo_no = "#[arcolinux_repo_testing]\n\
#SigLevel = Optional TrustedOnly\n\
#Include = /etc/pacman.d/arcolinux-mirrorlist"

arepo = "[arcolinux_repo]\n\
SigLevel = Optional TrustedOnly\n\
Include = /etc/pacman.d/arcolinux-mirrorlist"

a3drepo = "[arcolinux_repo_3party]\n\
SigLevel = Optional TrustedOnly\n\
Include = /etc/pacman.d/arcolinux-mirrorlist"

axlrepo = "[arcolinux_repo_xlarge]\n\
SigLevel = Optional TrustedOnly\n\
Include = /etc/pacman.d/arcolinux-mirrorlist"

chaotics_repo = "[chaotic-aur]\n\
SigLevel = Required DatabaseOptional\n\
Include = /etc/pacman.d/chaotic-mirrorlist"

endeavouros_repo = "[endeavouros]\n\
SigLevel = PackageRequired\n\
Include = /etc/pacman.d/endeavouros-mirrorlist"

nemesis_repo = "[nemesis_repo]\n\
SigLevel = Optional TrustedOnly\n\
Server = https://erikdubois.github.io/$repo/$arch"

xero_repo = "[xerolinux_repo]\n\
SigLevel = Optional TrustAll\n\
Include = /etc/pacman.d/xero-mirrorlist"

xero_xl_repo = "[xerolinux_repo_xl]\n\
SigLevel = Optional TrustAll\n\
Include = /etc/pacman.d/xero-mirrorlist"

xero_nv_repo = "[xerolinux_nvidia_repo]\n\
SigLevel = Optional TrustAll\n\
Include = /etc/pacman.d/xero-mirrorlist"

arch_testing_repo = "[core-testing]\n\
Include = /etc/pacman.d/mirrorlist"

arch_core_repo = "[core]\n\
Include = /etc/pacman.d/mirrorlist"

arch_extra_repo = "[extra]\n\
Include = /etc/pacman.d/mirrorlist"

arch_extra_testing_repo = "[extra-testing]\n\
Include = /etc/pacman.d/mirrorlist"

arch_multilib_testing_repo = "[multilib-testing]\n\
Include = /etc/pacman.d/mirrorlist"

reborn_repo = "[Reborn-OS]\n\
Include = /etc/pacman.d/reborn-mirrorlist"

leftwm_themes_list = [
    "arise",
    "candy",
    "db",
    "db-color-dev",
    "db-comic",
    "db-labels",
    "db-nemesis",
    "db-scifi",
    "docky",
    "doublebar",
    "eden",
    "forest",
    "grayblocks",
    "greyblocks",
    "halo",
    "kittycafe-dm",
    "kittycafe-sm",
    "material",
    "matrix",
    "mesh",
    "parker",
    "pi",
    "sb-horror",
    "shades",
    "smooth",
    "space",
    "starwars",
]

# =====================================================
#              END DECLARATION OF VARIABLES
# =====================================================
# =====================================================
# =====================================================
# =====================================================
# =====================================================
#               BEGIN GLOBAL FUNCTIONS
# =====================================================


def get_lines(files):
    try:
        if path.isfile(files):
            with open(files, "r", encoding="utf-8") as f:
                lines = f.readlines()
                f.close()
            return lines
    except Exception as error:
        print(error)


# get position in list


def get_position(lists, value):
    data = [string for string in lists if value in string]
    if len(data) != 0:
        position = lists.index(data[0])
        return position
    return 0


# get positions in list


def get_positions(lists, value):
    data = [string for string in lists if value in string]
    position = []
    for d in data:
        position.append(lists.index(d))
    return position


# get variable from list


def _get_variable(lists, value):
    data = [string for string in lists if value in string]

    if len(data) >= 1:
        data1 = [string for string in data if "#" in string]

        for i in data1:
            if i[:4].find("#") != -1:
                data.remove(i)
    if data:
        data_clean = [data[0].strip("\n").replace(" ", "")][0].split("=")
    return data_clean


# Check  value exists remove data


def check_value(list, value):
    data = [string for string in list if value in string]
    if len(data) >= 1:
        data1 = [string for string in data if "#" in string]
        for i in data1:
            if i[:4].find("#") != -1:
                data.remove(i)
    return data


# check backups


def check_backups(now):
    if not path.exists(home + "/" + bd + "/Backup-" + now.strftime("%Y-%m-%d %H")):
        makedirs(home + "/" + bd + "/Backup-" + now.strftime("%Y-%m-%d %H"), 0o777)
        permissions(home + "/" + bd + "/Backup-" + now.strftime("%Y-%m-%d %H"))


# check process is running


def check_if_process_is_running(processName):
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=["pid", "name", "create_time"])
            if processName == pinfo["name"]:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


# copytree


def copytree(self, src, dst, symlinks=False, ignore=None):  # noqa
    if not path.exists(dst):
        makedirs(dst)
    for item in listdir(src):
        s = path.join(src, item)
        d = path.join(dst, item)
        if path.exists(d):
            try:
                shutil.rmtree(d)
            except Exception as error:
                print(error)
                unlink(d)
        if path.isdir(s):
            try:
                shutil.copytree(s, d, symlinks, ignore)
            except Exception as error:
                print(error)
                print("ERROR2")
                self.ecode = 1
        else:
            try:
                shutil.copy2(s, d)
            except:  # noqa
                print("ERROR3")
                self.ecode = 1


# check lightdm value


def check_lightdm_value(list, value):
    data = [string for string in list if value in string]
    return data


# check sddm value


def check_sddm_value(list, value):
    data = [string for string in list if value in string]
    return data


# check if file exists


def file_check(file):
    if path.isfile(file):
        return True

    return False


# check if path exists


def path_check(path):
    if os.path.isdir(path):
        return True

    return False


# check if directory is empty


def is_empty_directory(path):
    if os.path.exists(path) and not os.path.isfile(path):
        if not os.listdir(path):
            # print("Empty directory")
            return True
        else:
            # print("Not empty directory")
            return False


# check if value is true or false in file


def check_content(value, file):
    try:
        with open(file, "r", encoding="utf-8") as myfile:
            lines = myfile.readlines()
            myfile.close()

        for line in lines:
            if value in line:
                if value in line:
                    return True
                else:
                    return False
        return False
    except:
        return False


# check if package is installed or not
def check_package_installed(package):  # noqa
    try:
        subprocess.check_output(
            "pacman -Qi " + package, shell=True, stderr=subprocess.STDOUT
        )
        # package is installed
        return True
    except subprocess.CalledProcessError:
        # package is not installed
        return False


# check if service is active


def check_service(service):  # noqa
    try:
        command = "systemctl is-active " + service + ".service"
        output = subprocess.run(
            command.split(" "),
            check=True,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        status = output.stdout.decode().strip()
        if status == "active":
            # print("Service is active")
            return True
        else:
            # print("Service is inactive")
            return False
    except Exception:
        return False


def check_socket(socket):  # noqa
    try:
        command = "systemctl is-active " + socket + ".socket"
        output = subprocess.run(
            command.split(" "),
            check=True,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        status = output.stdout.decode().strip()
        if status == "active":
            # print("Service is active")
            return True
        else:
            # print("Service is inactive")
            return False
    except Exception:
        return False


# list normal users


def list_users(filename):  # noqa
    try:
        data = []
        with open(filename, "r", encoding="utf-8") as f:
            for line in f.readlines():
                if "1001" in line.split(":")[2]:
                    data.append(line.split(":")[0])
                if "1002" in line.split(":")[2]:
                    data.append(line.split(":")[0])
                if "1003" in line.split(":")[2]:
                    data.append(line.split(":")[0])
                if "1004" in line.split(":")[2]:
                    data.append(line.split(":")[0])
                if "1005" in line.split(":")[2]:
                    data.append(line.split(":")[0])
            data.sort()
            return data
    except Exception as error:
        print(error)


# check if user is part of the group


def check_group(group):
    try:
        groups = subprocess.run(
            ["sh", "-c", "id " + sudo_username],
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        for x in groups.stdout.decode().split(" "):
            if group in x:
                return True
            else:
                return False
    except Exception as error:
        print(error)


def check_systemd_boot():
    if (
        path_check("/boot/loader") is True
        and file_check("/boot/loader/loader.conf") is True
    ):
        return True
    else:
        return False


# =====================================================
#               END GLOBAL FUNCTIONS
# =====================================================
# =====================================================
# =====================================================
# =====================================================


def check_arco_repos_active():
    with open(pacman, "r", encoding="utf-8") as f:
        lines = f.readlines()
        f.close()

        arco_base = "[arcolinux_repo]"
        arco_3p = "[arcolinux_repo_3party]"
        # arco_xl = "[arcolinux_repo_xlarge]"

    for line in lines:
        if arco_base in line:
            if "#" + arco_base in line:
                return False
            else:
                return True

    for line in lines:
        if arco_3p in line:
            if "#" + arco_3p in line:
                return False
            else:
                return True


def check_edu_repos_active():
    with open(pacman, "r", encoding="utf-8") as f:
        lines = f.readlines()
        f.close()

        nemesis = "[nemesis_repo]"

    for line in lines:
        if nemesis in line:
            if "#" + nemesis in line:
                return False
            else:
                return True


def install_package(self, package):
    command = "pacman -S " + package + " --noconfirm --needed"
    # if more than one package - checf fails and will install
    if check_package_installed(package):
        print(package + " is already installed - nothing to do")
        GLib.idle_add(
            show_in_app_notification,
            self,
            package + " is already installed - nothing to do",
        )
    else:
        try:
            print(command)
            subprocess.call(
                command.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            print(package + " is now installed")
            GLib.idle_add(show_in_app_notification, self, package + " is now installed")
        except Exception as error:
            print(error)


def install_local_package(self, package):
    command = "pacman -U " + package + " --noconfirm"
    # if more than one package - checf fails and will install
    try:
        print(command)
        subprocess.call(
            command.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print(package + " is now installed")
        GLib.idle_add(show_in_app_notification, self, package + " is now installed")
    except Exception as error:
        print(error)


def install_arco_package(self, package):
    if check_arco_repos_active():
        command = "pacman -S " + package + " --noconfirm --needed"
        if check_package_installed(package):
            print(package + " is already installed - nothing to do")
            GLib.idle_add(
                show_in_app_notification,
                self,
                package + " is already installed - nothing to do",
            )
        else:
            try:
                print(command)
                subprocess.call(
                    command.split(" "),
                    shell=False,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                )
                print(package + " is now installed")
                GLib.idle_add(
                    show_in_app_notification, self, package + " is now installed"
                )
            except Exception as error:
                print(error)
    else:
        print("You need to activate the ArcoLinux repos")
        print("Check the pacman tab of the ArchLinux Tweak Tool")
        print("and/or the content of /etc/pacman.conf")
        GLib.idle_add(
            show_in_app_notification, self, "You need to activate the ArcoLinux repos"
        )


def install_edu_package(self, package):
    if check_edu_repos_active():
        command = "pacman -S " + package + " --noconfirm --needed"
        if check_package_installed(package):
            print(package + " is already installed - nothing to do")
            GLib.idle_add(
                show_in_app_notification,
                self,
                package + " is already installed - nothing to do",
            )
        else:
            try:
                print(command)
                subprocess.call(
                    command.split(" "),
                    shell=False,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                )
                print(package + " is now installed")
                GLib.idle_add(
                    show_in_app_notification, self, package + " is now installed"
                )
            except Exception as error:
                print(error)
    else:
        print("You need to activate the Nemesis repo")
        print("Check the pacman tab of the ArchLinux Tweak Tool")
        print("and/or the content of /etc/pacman.conf")
        GLib.idle_add(
            show_in_app_notification, self, "You need to activate the Nemesis repo"
        )


def remove_package(self, package):
    command = "pacman -R " + package + " --noconfirm"
    if check_package_installed(package):
        print(command)
        try:
            subprocess.call(
                command.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            print(package + " is now removed")
            GLib.idle_add(show_in_app_notification, self, package + " is now removed")
        except Exception as error:
            print(error)
    else:
        print(package + " is already removed")
        GLib.idle_add(show_in_app_notification, self, package + " is already removed")


def remove_package_s(self, package):
    command = "pacman -Rs " + package + " --noconfirm"
    if check_package_installed(package):
        print(command)
        try:
            subprocess.call(
                command.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            print(package + " is now removed")
            GLib.idle_add(show_in_app_notification, self, package + " is now removed")
        except Exception as error:
            print(error)
    else:
        print(package + " is already removed")
        GLib.idle_add(show_in_app_notification, self, package + " is already removed")


def remove_package_ss(self, package):
    command = "pacman -Rss " + package + " --noconfirm"
    if check_package_installed(package):
        print(command)
        try:
            subprocess.call(
                command.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            print(package + " is now removed")
            GLib.idle_add(show_in_app_notification, self, package + " is now removed")
        except Exception as error:
            print(error)
    else:
        print(package + " is already removed")
        GLib.idle_add(show_in_app_notification, self, package + " is already removed")


def remove_package_dd(self, package):
    command = "pacman -Rdd " + package + " --noconfirm"
    if check_package_installed(package):
        print(command)
        try:
            subprocess.call(
                command.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            print(package + " is now removed")
            GLib.idle_add(show_in_app_notification, self, package + " is now removed")
        except Exception as error:
            print(error)
    else:
        print(package + " is already removed")
        GLib.idle_add(show_in_app_notification, self, package + " is already removed")


def remove_package_remnants(package):
    """remove theme.conf.user from folder - ATT shows names of empty folders"""
    # TODO: clean up for any theme
    # scan folders
    # if theme.conf is not present and theme.conf.user is delete
    if package == "arcolinux-meta-sddm-themes":
        themes = (
            "arcolinux-futuristic",
            "arcolinux-materia",
            "arcolinux-materia-dark",
            "arcolinux-simplicity",
            "arcolinux-slice",
            "arcolinux-sugar-candy",
            "arcolinux-urbanlifestyle",
        )
        for theme in themes:
            file = "/usr/share/sddm/themes/" + theme + "/theme.conf.user"
            directory = "/usr/share/sddm/themes/" + theme

            if file_check(file):
                print("Also remove - " + file)
                unlink(file)
                try:
                    rmdir(directory)
                except:
                    print("Manually remove any files in " + directory)

    # clean up two of the ATT themes
    # clean up if directory exists and if directory is not empty
    if check_package_installed("arcolinux-sddm-breeze-minimal-git") is False:
        file = "/usr/share/sddm/themes/arcolinux-breeze-minimal/theme.conf.user"
        directory = "/usr/share/sddm/themes/arcolinux-breeze-minimal"
        if path_check(directory):
            if file_check(file):
                try:
                    unlink(file)
                    if is_empty_directory(directory):
                        rmdir(directory)
                except:
                    print("Manually remove any files in " + directory)

    if check_package_installed("arcolinux-sddm-breeze-git") is False:
        file = "/usr/share/sddm/themes/arcolinux-breeze/theme.conf.user"
        directory = "/usr/share/sddm/themes/arcolinux-breeze"
        if path_check(directory):
            if file_check(file):
                try:
                    unlink(file)
                    if is_empty_directory(directory):
                        rmdir(directory)
                except:
                    print("Manually remove any files in " + directory)


def enable_login_manager(self, loginmanager):
    if check_package_installed(loginmanager):
        try:
            command = "systemctl enable " + loginmanager + ".service -f"
            print(command)
            subprocess.call(
                command.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            print(loginmanager + " has been enabled - reboot")
            GLib.idle_add(
                show_in_app_notification,
                self,
                loginmanager + " has been enabled - reboot",
            )
        except Exception as error:
            print(error)
    else:
        print(loginmanager + " is not installed")
        GLib.idle_add(
            show_in_app_notification, self, loginmanager + " is not installed"
        )


def add_autologin_group(self):
    com = subprocess.run(
        ["sh", "-c", "su - " + sudo_username + " -c groups"],
        check=True,
        shell=False,
        stdout=subprocess.PIPE,
    )
    groups = com.stdout.decode().strip().split(" ")
    # print(groups)
    if "autologin" not in groups:
        command = "groupadd autologin"
        try:
            subprocess.call(
                command.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
        except Exception as error:
            print(error)
        try:
            subprocess.run(
                ["gpasswd", "-a", sudo_username, "autologin"], check=True, shell=False
            )
        except Exception as error:
            print(error)


# =====================================================
#              CAJA SHARE PLUGIN
# =====================================================


def install_arco_caja_plugin(self, widget):
    # install = "pacman -S caja arcolinux-caja-share --noconfirm"
    install = "pacman -S caja caja-share --noconfirm"

    if check_package_installed("caja-share"):
        print("caja-share is already installed")
    else:
        subprocess.call(
            install.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print("Caja-share is now installed - reboot")
        GLib.idle_add(self.label7.set_text, "Caja-share is now installed - reboot")
    print("Other apps that might be interesting for sharing are :")
    print(" - thunar-share-plugin (thunar)")
    print(" - nemo-share (cinnamon)")
    print(" - nautilus-share (gnome - budgie)")
    print(" - kdenetwork-filesharing (plasma)")


# =====================================================
#              CHANGE SHELL
# =====================================================


def change_shell(self, shell):
    command = "sudo chsh " + sudo_username + " -s /bin/" + shell
    subprocess.call(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    print("Shell changed to " + shell + " for the user - logout")
    GLib.idle_add(
        show_in_app_notification,
        self,
        "Shell changed to " + shell + " for user - logout",
    )


# =====================================================
#               CONVERT COLOR
# =====================================================


def rgb_to_hex(rgb):
    if "rgb" in rgb:
        rgb = rgb.replace("rgb(", "").replace(")", "")
        vals = rgb.split(",")
        return "#{0:02x}{1:02x}{2:02x}".format(
            clamp(int(vals[0])), clamp(int(vals[1])), clamp(int(vals[2]))
        )
    return rgb


def clamp(x):
    return max(0, min(x, 255))


# =====================================================
#               COPY FUNCTION
# =====================================================


def copy_func(src, dst, isdir=False):
    if isdir:
        subprocess.run(["cp", "-Rp", src, dst], check=True, shell=False)
    else:
        subprocess.run(["cp", "-p", src, dst], check=True, shell=False)


# =====================================================
#               DISTRO LABEL
# =====================================================

# exceptions
if distr == "manjaro" and check_content("biglinux", "/etc/os-release"):
    distr = "biglinux"


def change_distro_label(name):  # noqa
    if name == "arcolinux":
        name = "ArcoLinux"
    if name == "biglinux":
        name = "BigLinux"
    if name == "garuda":
        name = "Garuda"
    if name == "endeavouros":
        name = "EndeavourOS"
    if name == "arch":
        name = "Arch Linux"
    if name == "manjaro":
        name = "Manjaro"
    if name == "xerolinux":
        name = "Xerolinux"
    if name == "axyl":
        name = "Axyl"
    if name == "rebornos":
        name = "RebornOS"
    if name == "amos":
        name = "AmOs"
    if name == "archcraft":
        name = "Archcraft"
    if name == "artix":
        name = "Artix"
    if name == "Archman":
        name = "ArchMan"
    if name == "cachyos":
        name = "CachyOS"
    return name


# ====================================================================
#                      GET DESKTOP
# ====================================================================

# def get_desktop(self):
#     base_dir = path.dirname(path.realpath(__file__))

#     desktop = subprocess.run(["sh", base_dir + "/get_desktop.sh", "-n"],
#                              shell=False,
#                              stdout=subprocess.PIPE,
#                              stderr=subprocess.STDOUT)
#     dsk = desktop.stdout.decode().strip().split("\n")
#     self.desktop = dsk[-1].strip()

# ====================================================================
#                      GRUB
# ====================================================================


def make_grub(self):
    try:
        command = "grub-mkconfig -o /boot/grub/grub.cfg"
        subprocess.call(
            command.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print("We will update your grub files")
        print("We update your grub with 'sudo grub-mkconfig -o /boot/grub/grub.cfg'")
        print("This can take a while...")
        show_in_app_notification(self, "We have updated your grub")
    except Exception as error:
        print(error)


# =====================================================
#               GRUB CONF
# =====================================================


def get_grub_wallpapers():
    if path.isdir("/boot/grub/themes/Vimix"):
        lists = listdir("/boot/grub/themes/Vimix")

        rems = [
            "select_e.png",
            "terminal_box_se.png",
            "select_c.png",
            "terminal_box_c.png",
            "terminal_box_s.png",
            "select_w.png",
            "terminal_box_nw.png",
            "terminal_box_w.png",
            "terminal_box_ne.png",
            "terminal_box_sw.png",
            "terminal_box_n.png",
            "terminal_box_e.png",
        ]

        ext = [".png", ".jpeg", ".jpg"]

        new_list = [x for x in lists if x not in rems for y in ext if y in x]

        new_list.sort()
        return new_list


def set_grub_wallpaper(self, image):
    if path.isfile(grub_theme_conf):
        if not path.isfile(grub_theme_conf + ".bak"):
            shutil.copy(grub_theme_conf, grub_theme_conf + ".bak")
        try:
            with open(grub_theme_conf, "r", encoding="utf-8") as f:
                lists = f.readlines()
                f.close()

            val = get_position(lists, "desktop-image: ")
            lists[val] = 'desktop-image: "' + path.basename(image) + '"' + "\n"

            with open(grub_theme_conf, "w", encoding="utf-8") as f:
                f.writelines(lists)
                f.close()
            print("Grub wallpaper saved")
            print(image)
            show_in_app_notification(self, "Grub wallpaper saved")
        except:
            pass


def set_login_wallpaper(self, image):
    # if sddm
    if self.login_managers_combo.get_active_text() == "sddm":
        if path.isfile(sddm_default_d2):
            try:
                with open(sddm_default_d2, "r", encoding="utf-8") as f:
                    lists = f.readlines()
                    f.close()
                val = get_position(lists, "Current=")
                theme = lists[val].strip("\n").split("=")[1]
            except:
                pass

            if not path.isfile("/usr/share/sddm/themes/" + theme + "/theme.conf.user"):
                try:
                    with open(
                        "/usr/share/sddm/themes/" + theme + "/theme.conf.user",
                        "w",
                        encoding="utf-8",
                    ) as f:
                        f.write("[General]\n")
                        f.write("background=\n")
                        f.write("type=image\n")
                        f.close()
                    print("Created theme.conf.user for " + theme)
                except:
                    pass

            if path.isfile("/usr/share/sddm/themes/" + theme + "/theme.conf.user"):
                try:
                    print("This is your current theme: " + theme)
                    with open(
                        "/usr/share/sddm/themes/" + theme + "/theme.conf.user",
                        "r",
                        encoding="utf-8",
                    ) as f:
                        lists = f.readlines()
                        f.close()

                    val = get_position(lists, "background=")
                    lists[val] = "background=" + image + "\n"
                    print(lists[val])

                    with open(
                        "/usr/share/sddm/themes/" + theme + "/theme.conf.user",
                        "w",
                        encoding="utf-8",
                    ) as f:
                        f.writelines(lists)
                        f.close()
                    print("Login wallpaper saved")
                    show_in_app_notification(self, "Login wallpaper saved")
                except:
                    pass
        else:
            print("There is no /etc/sddm.conf.d/kde_settings.conf")
            show_in_app_notification(self, "Use the ATT sddm configuration")

    # if lightdm
    if self.login_managers_combo.get_active_text() == "lightdm":
        if path.isfile(lightdm_greeter):
            try:
                with open(lightdm_greeter, "r", encoding="utf-8") as f:
                    lists = f.readlines()
                    f.close()

                val = get_position(lists, "background=")
                lists[val] = "background=" + image + "\n"
                print(lists[val])

                with open(lightdm_greeter, "w", encoding="utf-8") as f:
                    f.writelines(lists)
                    f.close()
                print("Login wallpaper saved to /etc/lightdm/lightdm-gtk-greeter.conf")
                show_in_app_notification(self, "Login wallpaper saved")
            except:
                pass
        else:
            print("There is no /etc/lightdm/lightdm-gtk-greeter.conf")
            show_in_app_notification(
                self, "There is no /etc/lightdm/lightdm-gtk-greeter.conf"
            )

        if path.isfile(lightdm_slick_greeter):
            try:
                with open(lightdm_slick_greeter, "r", encoding="utf-8") as f:
                    lists = f.readlines()
                    f.close()

                val = get_position(lists, "background=")
                lists[val] = "background=" + image + "\n"
                print(lists[val])

                with open(lightdm_slick_greeter, "w", encoding="utf-8") as f:
                    f.writelines(lists)
                    f.close()
                print("Login wallpaper saved to /etc/lightdm/slick-greeter.conf")
                show_in_app_notification(self, "Login wallpaper saved")
            except:
                pass
        else:
            print("There is no /etc/lightdm/lightdm-gtk-greeter.conf")
            show_in_app_notification(
                self, "There is no /etc/lightdm/lightdm-gtk-greeter.conf"
            )

    # if lxdm
    if self.login_managers_combo.get_active_text() == "lxdm":
        if path.isfile(lxdm_conf):
            try:
                with open(lxdm_conf, "r", encoding="utf-8") as f:
                    lists = f.readlines()
                    f.close()

                val = get_position(lists, "bg=")
                lists[val] = "bg=" + image + "\n"
                print(lists[val])

                with open(lxdm_conf, "w", encoding="utf-8") as f:
                    f.writelines(lists)
                    f.close()
                print("Login wallpaper saved to /etc/lxdm/lxdm.conf")
                show_in_app_notification(self, "Login wallpaper saved")
            except:
                pass
        else:
            print("There is no /etc/lxdm/lxdm.conf")
            show_in_app_notification(self, "There is no /etc/lxdm/lxdm.conf")


def reset_login_wallpaper(self, image):
    if path.isfile(sddm_default_d2):
        try:
            with open(sddm_default_d2, "r", encoding="utf-8") as f:
                lists = f.readlines()
                f.close()
            val = get_position(lists, "Current=")
            theme = lists[val].strip("\n").split("=")[1]
        except:
            pass

    if path.isfile("/usr/share/sddm/themes/" + theme + "/theme.conf.user"):
        try:
            unlink("/usr/share/sddm/themes/" + theme + "/theme.conf.user")
            print("Standard background has been reset")
            show_in_app_notification(self, "Background reset successfully")
        except:
            pass


def set_default_grub_theme(self):
    if path.isfile(grub_default_grub):
        if not path.isfile(grub_default_grub + ".back"):
            shutil.copy(grub_default_grub, grub_default_grub + ".back")
        try:
            with open(grub_default_grub, "r", encoding="utf-8") as f:
                grubd = f.readlines()
                f.close()

            try:
                val = get_position(grubd, "GRUB_THEME")
                grubd[val] = 'GRUB_THEME="/boot/grub/themes/Vimix/theme.txt"\n'
            except IndexError:
                pass

            with open(grub_default_grub, "w", encoding="utf-8") as f:
                f.writelines(grubd)
                f.close()

            print("Grub settings saved successfully in /etc/default/grub")
            print("We made sure you have a backup - /etc/default/grub.back")
            print("This line has changed in /etc/default/grub")
            print('GRUB_THEME="/boot/grub/themes/Vimix/theme.txt"')

            show_in_app_notification(self, "Grub settings saved in /etc/default/grub")
        except Exception as error:
            print(error)


def set_grub_timeout(self, number):
    try:
        with open(grub_default_grub, "r", encoding="utf-8") as f:
            lists = f.readlines()
            f.close()

        val = get_position(lists, "GRUB_TIMEOUT=")
        lists[val] = "GRUB_TIMEOUT=" + str(number) + "\n"
        print(lists[val])

        with open(grub_default_grub, "w", encoding="utf-8") as f:
            f.writelines(lists)
            f.close()
        print("Grub timeout in seconds saved - /etc/default/grub")
        show_in_app_notification(self, "Grub timeout in seconds saved")
    except Exception as error:
        print(error)


# =====================================================
#               GTK3 CONF
# =====================================================

# def gtk_check_value(my_list, value):
#     data = [string for string in my_list if value in string]
#     if len(data) >= 1:
#         data1 = [string for string in data if "#" in string]
#         for i in data1:
#             if i[:4].find('#') != -1:
#                 data.remove(i)
#     return data


# def gtk_get_position(my_list, value):
#     data = [string for string in my_list if value in string]
#     position = my_list.index(data[0])
#     return position

# =====================================================
#               HBLOCK CONF
# =====================================================


def hblock_get_state(self):
    lines = int(
        subprocess.check_output("wc -l /etc/hosts", shell=True).strip().split()[0]
    )
    if path.exists("/usr/bin/hblock") and lines > 100:
        return True

    self.firstrun = False
    return False


def do_pulse(data, prog):
    prog.pulse()
    return True


def set_hblock(self, toggle, state):
    GLib.idle_add(toggle.set_sensitive, False)
    GLib.idle_add(self.label7.set_text, "Run..")
    GLib.idle_add(self.progress.set_fraction, 0.2)

    timeout_id = None
    timeout_id = GLib.timeout_add(100, do_pulse, None, self.progress)

    if not path.isfile("/etc/hosts.bak"):
        shutil.copy("/etc/hosts", "/etc/hosts.bak")

    try:
        install = "pacman -S arcolinux-hblock-git --needed --noconfirm"
        enable = "/usr/bin/hblock"

        if state:
            if path.exists("/usr/bin/hblock"):
                GLib.idle_add(self.label7.set_text, "Database update...")
                subprocess.call(
                    [enable],
                    shell=False,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                )
            else:
                GLib.idle_add(self.label7.set_text, "Install Hblock......")
                subprocess.call(
                    install.split(" "),
                    shell=False,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                )
                GLib.idle_add(self.label7.set_text, "Database update...")
                subprocess.call(
                    [enable],
                    shell=False,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                )

        else:
            GLib.idle_add(self.label7.set_text, "Remove update...")
            subprocess.run(
                ["sh", "-c", "HBLOCK_SOURCES='' /usr/bin/hblock"],
                check=True,
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )

        GLib.idle_add(self.label7.set_text, "Complete")
        GLib.source_remove(timeout_id)
        timeout_id = None
        GLib.idle_add(self.progress.set_fraction, 0)

        GLib.idle_add(toggle.set_sensitive, True)
        if state:
            GLib.idle_add(self.label7.set_text, "HBlock Active")
        else:
            GLib.idle_add(self.label7.set_text, "HBlock Inactive")

    except Exception as error:
        messagebox(self, "ERROR!!", str(error))
        print(error)


# =====================================================
#               LIGHTDM SLICK GREETER
# =====================================================


def enable_slick_greeter(self):
    if path.isfile(lightdm_conf):
        try:
            with open(lightdm_conf, "r", encoding="utf-8") as f:
                lists = f.readlines()
                f.close()

            val = get_position(lists, "#greeter-session=example-gtk-gnome")
            lists[val] = "greeter-session=lightdm-slick-greeter" + "\n"

            with open(lightdm_conf, "w", encoding="utf-8") as f:
                f.writelines(lists)
                f.close()
        except Exception as error:
            print(error)


def disable_slick_greeter(self):
    if path.isfile(lightdm_conf):
        try:
            with open(lightdm_conf, "r", encoding="utf-8") as f:
                lists = f.readlines()
                f.close()

            val = get_position(lists, "greeter-session=lightdm-slick-greeter")
            lists[val] = "#greeter-session=example-gtk-gnome" + "\n"

            with open(lightdm_conf, "w", encoding="utf-8") as f:
                f.writelines(lists)
                f.close()
        except Exception as error:
            print(error)


# =====================================================
#               LOG FILE CREATION
# =====================================================


log_dir = "/var/log/archlinux/"
att_log_dir = "/var/log/archlinux/att/"


def create_log(self):
    print("Making log in /var/log/archlinux")
    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d-%H-%M-%S")
    destination = att_log_dir + "att-log-" + time
    command = "sudo pacman -Q > " + destination
    subprocess.call(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    # GLib.idle_add(show_in_app_notification, self, "Log file created")


# =====================================================
#               LOGIN WALL
# =====================================================


def get_login_wallpapers():
    if path.isdir(login_backgrounds):
        lists = listdir(login_backgrounds)

        rems = [
            "select_e.png",
            "terminal_box_se.png",
            "select_c.png",
            "terminal_box_c.png",
            "terminal_box_s.png",
            "select_w.png",
            "terminal_box_nw.png",
            "terminal_box_w.png",
            "terminal_box_ne.png",
            "terminal_box_sw.png",
            "terminal_box_n.png",
            "terminal_box_e.png",
        ]

        ext = [".png", ".jpeg", ".jpg"]

        new_list = [x for x in lists if x not in rems for y in ext if y in x]

        new_list.sort()
        return new_list


# =====================================================
#               MESSAGEBOX
# =====================================================


def messagebox(self, title, message):
    md2 = Gtk.MessageDialog(
        parent=self,
        flags=0,
        message_type=Gtk.MessageType.INFO,
        buttons=Gtk.ButtonsType.OK,
        text=message,
    )
    md2.format_secondary_markup(message)
    md2.run()
    md2.destroy()


# =====================================================
#              NEMO SHARE PLUGIN
# =====================================================


def install_arco_nemo_plugin(self, widget):
    # install = "pacman -S nemo arcolinux-nemo-share --noconfirm"
    install = "pacman -S nemo nemo-share --noconfirm"

    if check_package_installed("nemo-share"):
        print("Nemo-share is already installed")
    else:
        subprocess.call(
            install.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print("Nemo-share is now installed - reboot")
        GLib.idle_add(self.label7.set_text, "Nemo-share is now installed - reboot")
    print("Other apps that might be interesting for sharing are :")
    print(" - thunar-share-plugin (thunar)")
    print(" - caja-share (mate)")
    print(" - kdenetwork-filesharing (plasma)")
    print(" - nautilus-share (gnome - budgie)")


# =====================================================
#               NEOFETCH CONF
# =====================================================


def neofetch_set_value(lists, pos, text, state):
    if state:
        if text in lists[pos]:
            if "#" in lists[pos]:
                lists[pos] = lists[pos].replace("#", "")
    else:
        if text in lists[pos]:
            if "#" not in lists[pos]:
                lists[pos] = "#" + lists[pos]

    return lists


def neofetch_set_backend_value(lists, pos, text, value):
    if text in lists[pos] and "#" not in lists[pos]:
        lists[pos] = text + value + '"\n'


# =====================================================
#               NOTIFICATIONS
# =====================================================


def show_in_app_notification(self, message):
    if self.timeout_id is not None:
        GLib.source_remove(self.timeout_id)
        self.timeout_id = None

    self.notification_label.set_markup(
        '<span foreground="white">' + message + "</span>"
    )
    self.notification_revealer.set_reveal_child(True)
    self.timeout_id = GLib.timeout_add(3000, timeOut, self)


def timeOut(self):
    close_in_app_notification(self)


def close_in_app_notification(self):
    self.notification_revealer.set_reveal_child(False)
    GLib.source_remove(self.timeout_id)
    self.timeout_id = None


# =====================================================
#               NSSWITCH CONF COPY
# =====================================================


def copy_nsswitch(choice):
    command = (
        "cp /usr/share/archlinux-tweak-tool/data/"
        + choice
        + "/nsswitch.conf /etc/nsswitch.conf"
    )
    print(command)
    subprocess.call(
        command.split(" "),
        shell=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    print("/etc/nsswitch.conf has been overwritten - reboot")


# =====================================================
#               OBLOGOUT CONF
# =====================================================
# Get shortcuts index


def get_shortcuts(conflist):
    sortcuts = _get_variable(conflist, "shortcuts")
    shortcuts_index = get_position(conflist, sortcuts[0])
    return int(shortcuts_index)


# Get commands index


def get_commands(conflist):
    commands = _get_variable(conflist, "commands")
    commands_index = get_position(conflist, commands[0])
    return int(commands_index)


# =====================================================
#               PACE INSTALLATION
# =====================================================


def install_pace(self):
    install = "pacman -S pace --noconfirm --needed"

    if path.exists("/usr/bin/pace"):
        # print("Pace is already installed")
        pass
    else:
        try:
            subprocess.call(
                install.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            print("Pace is now installed")
        except Exception as error:
            print(error)


# =====================================================
#               PACMAN EXTRA KEYS AND MIRRORS
# =====================================================


def install_reborn(self):
    base_dir = path.dirname(path.realpath(__file__))
    pathway = base_dir + "/data/reborn/packages/keyring/"
    file = listdir(pathway)
    try:
        install = "pacman -U " + pathway + str(file).strip("[]'") + " --noconfirm"
        print(install)
        subprocess.call(
            install.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print("RebornOS keyring is now installed")
    except Exception as error:
        print(error)

    base_dir = path.dirname(path.realpath(__file__))
    pathway = base_dir + "/data/reborn/packages/mirrorlist/"
    file = listdir(pathway)
    try:
        install = "pacman -U " + pathway + str(file).strip("[]'") + " --noconfirm"
        print(install)
        subprocess.call(
            install.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print("RebornOS mirrorlist is now installed")
    except Exception as error:
        print(error)


def install_chaotics(self):
    base_dir = path.dirname(path.realpath(__file__))
    pathway = base_dir + "/data/garuda/packages/keyring/"
    file = listdir(pathway)
    try:
        install = "pacman -U " + pathway + str(file).strip("[]'") + " --noconfirm"
        print(install)
        subprocess.call(
            install.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print("Chaotics keyring is now installed")
    except Exception as error:
        print(error)

    base_dir = path.dirname(path.realpath(__file__))
    pathway = base_dir + "/data/garuda/packages/mirrorlist/"
    file = listdir(pathway)
    try:
        install = "pacman -U " + pathway + str(file).strip("[]'") + " --noconfirm"
        print(install)
        subprocess.call(
            install.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print("Chaotics mirrorlist is now installed")
    except Exception as error:
        print(error)


def install_endeavouros(self):
    base_dir = path.dirname(path.realpath(__file__))
    pathway = base_dir + "/data/eos/packages/keyring/"
    file = listdir(pathway)
    try:
        install = "pacman -U " + pathway + str(file).strip("[]'") + " --noconfirm"
        print(install)
        subprocess.call(
            install.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print("EndeavourOS keyring is now installed")
    except Exception as error:
        print(error)

    base_dir = path.dirname(path.realpath(__file__))
    pathway = base_dir + "/data/eos/packages/mirrorlist/"
    file = listdir(pathway)
    try:
        install = "pacman -U " + pathway + str(file).strip("[]'") + " --noconfirm"
        print(install)
        subprocess.call(
            install.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print("EndeavourOS mirrorlist is now installed")
    except Exception as error:
        print(error)


def install_arcolinux(self):
    base_dir = path.dirname(path.realpath(__file__))
    pathway = base_dir + "/data/arco/packages/keyring/"
    file = listdir(pathway)

    try:
        install = "pacman -U " + pathway + str(file).strip("[]'") + " --noconfirm"
        print(install)
        subprocess.call(
            install.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print("ArcoLinux keyring is now installed")
    except Exception as error:
        print(error)

    pathway = base_dir + "/data/arco/packages/mirrorlist/"
    file = listdir(pathway)
    try:
        install = "pacman -U " + pathway + str(file).strip("[]'") + " --noconfirm"
        print(install)
        subprocess.call(
            install.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print("ArcoLinux mirrorlist is now installed")
    except Exception as error:
        print(error)

    """add the ArcoLinux repos in /etc/pacman.conf if none are present"""
    if not check_content("arcolinux", pacman):
        if distr == "arcolinux":
            print("[INFO] : Adding ArcoLinux repos on ArcoLinux")
            try:
                with open(pacman, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    f.close()
            except Exception as error:
                print(error)

            text = (
                "\n\n"
                + atestrepo_no
                + "\n\n"
                + arepo
                + "\n\n"
                + a3drepo
                + "\n\n"
                + axlrepo
            )

            pos = get_position(lines, "#[testing]")
            lines.insert(pos - 2, text)

            try:
                with open(pacman, "w", encoding="utf-8") as f:
                    f.writelines(lines)
            except Exception as error:
                print(error)


def install_xerolinux(self):
    base_dir = path.dirname(path.realpath(__file__))
    pathway = base_dir + "/data/xero/packages/mirrorlist/"
    file = listdir(pathway)
    try:
        install = "pacman -U " + pathway + str(file).strip("[]'") + " --noconfirm"
        print(install)
        subprocess.call(
            install.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print("Xerolinux mirrorlist is now installed")
    except Exception as error:
        print(error)


# =====================================================
#               PERMISSIONS
# =====================================================


def test(dst):
    for root, dirs, filesr in walk(dst):
        # print(root)
        for folder in dirs:
            pass
            # print(dst + "/" + folder)
            for file in filesr:
                pass
                # print(dst + "/" + folder + "/" + file)
        for file in filesr:
            pass
            # print(dst + "/" + file)


def permissions(dst):
    try:
        groups = subprocess.run(
            ["sh", "-c", "id " + sudo_username],
            check=True,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        for x in groups.stdout.decode().split(" "):
            if "gid" in x:
                g = x.split("(")[1]
                group = g.replace(")", "").strip()
        subprocess.call(["chown", "-R", sudo_username + ":" + group, dst], shell=False)
    except Exception as error:
        print(error)


# =====================================================
#               RESTART PROGRAM
# =====================================================


def restart_program():
    if path.exists("/tmp/att.lock"):
        unlink("/tmp/att.lock")
        python = sys.executable
        execl(python, python, *sys.argv)


# =====================================================
#               SERVICES - GENERAL FUNCTIONS CUPS
# =====================================================


def enable_service(service):
    try:
        command = "systemctl enable " + service + ".service -f --now"
        subprocess.call(
            command.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print("We enabled the following service : " + service)
    except Exception as error:
        print(error)


def restart_service(service):
    try:
        command = "systemctl reload-or-restart " + service + ".service"
        subprocess.call(
            command.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print("We restarted the following service (if avalable) : " + service)
    except Exception as error:
        print(error)


def disable_service(service):
    try:
        command = "systemctl stop " + service
        subprocess.call(
            command.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        command = "systemctl disable " + service
        subprocess.call(
            command.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print("We stopped and disabled the following service " + service)
    except Exception as error:
        print(error)


def find_active_audio():
    output = subprocess.run(["pactl", "info"], check=True, stdout=subprocess.PIPE)

    pipewire_active = check_value(output, "pipewire")

    if pipewire_active == True:
        return pipewire_active
    else:
        return pipewire_active


# =====================================================
#               SERVICES - AVAHI
# =====================================================


def install_discovery(self):
    try:
        install = "pacman -S avahi nss-mdns gvfs-smb --needed --noconfirm"

        if (
            check_package_installed("avahi")
            and check_package_installed("nss-mdns")
            and check_package_installed("gvfs-smb")
        ):
            pass
        else:
            subprocess.call(
                install.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            print("Avahi, nss-mdns and gvfs-smb is now installed")

        command = "systemctl enable avahi-daemon.service -f --now"
        subprocess.call(
            command.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print("We enabled avahi-daemon.service")
    except Exception as error:
        print(error)


def remove_discovery(self):
    try:
        command = "systemctl stop avahi-daemon.service -f --now"
        subprocess.call(
            command.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        command = "systemctl disable avahi-daemon.service -f --now"
        subprocess.call(
            command.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print("We disabled avahi-daemon.service")

        command = "systemctl stop avahi-daemon.socket -f"
        subprocess.call(
            command.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        command = "systemctl disable avahi-daemon.socket -f"
        subprocess.call(
            command.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print("We disabled avahi-daemon.socket")

        command = "pacman -Rs avahi --noconfirm"
        if check_package_installed("avahi"):
            subprocess.call(
                command.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            print("Avahi was removed")

        command = "pacman -Rs nss-mdns --noconfirm"
        if check_package_installed("nss-mdns"):
            subprocess.call(
                command.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            print("nss-mdns was removed")

        command = "pacman -Rs gvfs-smb --noconfirm"
        if check_package_installed("gvfs-smb"):
            subprocess.call(
                command.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            print("gvfs-smb was removed")
        else:
            pass
    except Exception as error:
        print(error)


# =====================================================
#               SERVICES - SAMBA
# =====================================================


def install_samba(self):
    try:
        install = "pacman -S samba gvfs-smb --needed --noconfirm"

        if not path.isdir("/var/cache/samba"):
            makedirs("/var/cache/samba", 0o755)

        if check_package_installed("samba") and check_package_installed("gvfs-smb"):
            pass
        else:
            subprocess.call(
                install.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            print("Samba and gvfs-smb are now installed")

        command = "systemctl enable smb.service -f --now"
        subprocess.call(
            command.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print("We enabled smb.service")

        command = "systemctl enable nmb.service -f --now"
        subprocess.call(
            command.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print("We enabled nmb.service")
    except Exception as error:
        print(error)


def uninstall_samba(self):
    try:
        command = "systemctl disable smb.service -f --now"
        subprocess.call(
            command.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print("We disabled smb.service")

        command = "systemctl disable nmb.service -f --now"
        subprocess.call(
            command.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print("We disabled nmb.service")

        command = "pacman -Rs samba --noconfirm"
        if check_package_installed("samba"):
            subprocess.call(
                command.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            print("Samba was removed if there were no dependencies")

        command = "pacman -Rs gvfs-smb --noconfirm"
        if check_package_installed("nss-mdns"):
            subprocess.call(
                command.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            print("gvfs-smb was removed")
    except Exception as error:
        print(error)


# =====================================================
#               SAMBA CONF COPY
# =====================================================


def copy_samba(choice):
    command = (
        "cp /usr/share/archlinux-tweak-tool/data/any/samba/"
        + choice
        + "/smb.conf /etc/samba/smb.conf"
    )
    subprocess.call(
        command.split(" "),
        shell=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if choice == "example":
        if not path.isdir("/home/" + sudo_username + "/Shared"):
            makedirs("/home/" + sudo_username + "/Shared", 0o755)
        permissions("/home/" + sudo_username + "/Shared")
        try:
            with open(samba_config, "r", encoding="utf-8") as f:
                lists = f.readlines()
                f.close()

            val = get_position(lists, "[SAMBASHARE]")
            lists[val + 1] = "path = " + "/home/" + sudo_username + "/Shared\n"

            print("You have choosen for the easy setup")
            print("We have added a folder called 'Shared' to your home directory")
            print("You can access this folder from any computer in your network")
            print("You can write and remove items from the shared folder")
            print("Reboot or restart smb first")
            print(lists[val + 1])

            with open(samba_config, "w", encoding="utf-8") as f:
                f.writelines(lists)
                f.close()
        except Exception as error:
            print(error)

    if choice == "usershares":
        # make folder
        if not path.isdir("/var/lib/samba/usershares"):
            makedirs("/var/lib/samba/usershares", 0o770)

        # create system sambashare group
        try:
            if check_group("sambashare"):
                pass
            else:
                try:
                    command = "groupadd -r sambashare"
                    subprocess.call(
                        command.split(" "),
                        shell=False,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                    )
                except Exception as error:
                    print(error)

        except Exception as error:
            print(error)

        # add user to group
        try:
            command = "gpasswd -a " + sudo_username + " sambashare"
            subprocess.call(
                command.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
        except Exception as error:
            print(error)

        try:
            command = "chown root:sambashare /var/lib/samba/usershares"
            subprocess.call(
                command.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
        except Exception as error:
            print(error)

        try:
            command = "chmod 1770 /var/lib/samba/usershares"
            subprocess.call(
                command.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
        except Exception as error:
            print(error)


# =====================================================
#               SAMBA EDIT
# =====================================================


# samba advanced - TODO
def save_samba_config(self):
    # create smb.conf if there is none?
    if path.isfile(samba_config):
        if not path.isfile(samba_config + ".bak"):
            shutil.copy(samba_config, samba_config + ".bak")
        try:
            with open(samba_config, "r", encoding="utf-8") as f:
                lists = f.readlines()
                f.close()

            path = self.entry_path.get_text()
            browseable = self.samba_share_browseable.get_active()
            if browseable:
                browseable = "yes"
            else:
                browseable = "no"
            guest = self.samba_share_guest.get_active()
            if guest:
                guest = "yes"
            else:
                guest = "no"
            public = self.samba_share_public.get_active()
            if public:
                public = "yes"
            else:
                public = "no"
            writable = self.samba_share_writable.get_active()
            if writable:
                writable = "yes"
            else:
                writable = "no"

            val = get_position(lists, "[SAMBASHARE]")
            if lists[val] == ";[SAMBASHARE]\n":
                lists[val] = "[SAMBASHARE]" + "\n"
            lists[val + 1] = "path = " + path + "\n"
            lists[val + 2] = "browseable  = " + browseable + "\n"
            lists[val + 3] = "guest ok = " + guest + "\n"
            lists[val + 4] = "public = " + public + "\n"
            lists[val + 5] = "writable = " + writable + "\n"

            print("These lines have been saved at the end of /etc/samba/smb.conf")
            print("Edit this file to add more shares")
            print(lists[val])
            print(lists[val + 1])
            print(lists[val + 2])
            print(lists[val + 3])
            print(lists[val + 4])
            print(lists[val + 5])

            with open(samba_config, "w", encoding="utf-8") as f:
                f.writelines(lists)
                f.close()

            print("Smb.conf has been saved")
            show_in_app_notification(self, "Smb.conf has been saved")
        except:
            pass
    else:
        print(
            "Choose or create your own smb.conf in /etc/samba/smb.conf then change settings"
        )
        show_in_app_notification(self, "Choose or create your own smb.conf")


# =====================================================
#                       SDDM
# =====================================================


def create_sddm_k_dir():
    if not path.isdir(sddm_default_d2_dir):
        try:
            mkdir(sddm_default_d2_dir)
        except Exception as error:
            print(error)


# =====================================================
#                       SHELL
# =====================================================


def source_shell(self):
    process = subprocess.run(
        ["sh", "-c", 'echo "$SHELL"'], check=True, stdout=subprocess.PIPE
    )

    output = process.stdout.decode().strip()
    if output == "/bin/bash":
        subprocess.run(
            [
                "bash",
                "-c",
                "su - " + sudo_username + ' -c "source ' + home + '/.bashrc"',
            ],
            check=True,
            stdout=subprocess.PIPE,
        )
    elif output == "/bin/zsh":
        subprocess.run(
            ["zsh", "-c", "su - " + sudo_username + ' -c "source ' + home + '/.zshrc"'],
            check=True,
            stdout=subprocess.PIPE,
        )
    elif output == "/usr/bin/fish":
        subprocess.run(
            [
                "fish",
                "-c",
                "su - "
                + sudo_username
                + ' -c "source '
                + home
                + '/.config/fish/config.fish"',
            ],
            check=True,
            stdout=subprocess.PIPE,
        )


def get_shell():
    try:
        process = subprocess.run(
            ["su", "-", sudo_username, "-c", 'echo "$SHELL"'],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        output = process.stdout.decode().strip().strip("\n")
        if output in ("/bin/bash", "/usr/bin/bash"):
            return "bash"
        elif output in ("/bin/zsh", "/usr/bin/zsh"):
            return "zsh"
        elif output in ("/bin/fish", "/usr/bin/fish"):
            return "fish"
    except Exception as error:
        print(error)


def run_as_user(script):
    subprocess.call(["su - " + sudo_username + " -c " + script], shell=False)


# def install_extra_shell(package):
#     install = "pacman -S " + package + " --needed --noconfirm"
#     print(install)
#     try:
#         subprocess.call(
#             install.split(" "),
#             shell=False,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.STDOUT,
#         )
#     except Exception as error:
#         print(error)


# =====================================================
#               THUNAR SHARE PLUGIN
# =====================================================


def install_arco_thunar_plugin(self, widget):
    # install = "pacman -S thunar arcolinux-thunar-shares-plugin --noconfirm"
    install = "pacman -S thunar thunar-shares-plugin --noconfirm"

    if check_package_installed("thunar-shares-plugin"):
        print("Thunar-shares-plugin is already installed")
    else:
        try:
            subprocess.call(
                install.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            print("Thunar-shares-plugin is now installed - reboot")
            GLib.idle_add(
                self.label7.set_text,
                "Thunar-shares-plugin is now installed - reboot",
            )
            print("Other apps that might be interesting for sharing are :")
            print(" - arcolinux-nemo-share (cinnamon)")
            print(" - arcolinux-caja-share (mate)")
            print(" - arcolinux-nautilus-share (gnome - budgie)")
            print(" - kdenetwork-filesharing (plasma)")

        except Exception as error:
            print(error)


# =====================================================
#               UBLOCK ORIGIN
# =====================================================


def ublock_get_state(self):
    if path.exists("/usr/lib/firefox/browser/extensions/uBlock0@raymondhill.net.xpi"):
        return True
    return False


def set_firefox_ublock(self, toggle, state):
    GLib.idle_add(toggle.set_sensitive, False)
    GLib.idle_add(self.label7.set_text, "Run..")
    GLib.idle_add(self.progress.set_fraction, 0.2)

    timeout_id = None
    timeout_id = GLib.timeout_add(100, do_pulse, None, self.progress)

    try:
        install_ublock = "pacman -S firefox-ublock-origin --needed --noconfirm"
        uninstall_ublock = "pacman -Rs firefox-ublock-origin --noconfirm"

        if state:
            GLib.idle_add(self.label7.set_text, "Installing ublock Origin...")
            subprocess.call(
                install_ublock.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
        else:
            GLib.idle_add(self.label7.set_text, "Removing ublock Origin...")
            subprocess.call(
                uninstall_ublock.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )

        GLib.idle_add(self.label7.set_text, "Complete")
        GLib.source_remove(timeout_id)
        timeout_id = None
        GLib.idle_add(self.progress.set_fraction, 0)

        GLib.idle_add(toggle.set_sensitive, True)
        if state:
            GLib.idle_add(self.label7.set_text, "uBlock Origin installed")
        else:
            GLib.idle_add(self.label7.set_text, "uBlock Origin removed")

    except Exception as error:
        messagebox(self, "ERROR!!", str(error))
        print(error)


# ====================================================================
#                      UPDATE REPOS
# ====================================================================


def update_repos(self):
    try:
        command = "pacman -Sy"
        subprocess.call(
            command.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        # print("Getting the databases in from all repositories")
        # show_in_app_notification(self, "Dowloading repo libraries")
    except Exception as error:
        print(error)


# =====================================================
#               WALL
# =====================================================


def install_archlinux_login_backgrounds(self, widget):
    install = "pacman -S archlinux-login-backgrounds-git --noconfirm"

    if check_package_installed("archlinux-login-backgrounds-git"):
        print("Archlinux-login-backgrounds-git is already installed")
        GLib.idle_add(
            show_in_app_notification,
            self,
            "Archlinux-login-backgrounds-git is already installed",
        )
    else:
        try:
            subprocess.call(
                install.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            print("Archlinux-login-backgrounds-git is now installed")
            GLib.idle_add(
                show_in_app_notification,
                self,
                "Archlinux-login-backgrounds-git is now installed",
            )

        except Exception as error:
            print(error)


def remove_archlinux_login_backgrounds(self, widget):
    install = "pacman -R archlinux-login-backgrounds-git --noconfirm"

    if check_package_installed("archlinux-login-backgrounds-git"):
        try:
            subprocess.call(
                install.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            print("Archlinux-login-backgrounds-git is now removed")
            GLib.idle_add(
                show_in_app_notification,
                self,
                "Archlinux-login-backgrounds-git is now installed",
            )

        except Exception as error:
            print(error)
    else:
        print("Archlinux-login-backgrounds-git is already removed")
        GLib.idle_add(
            show_in_app_notification, self, "Archlinux-login-backgrounds-git is removed"
        )
