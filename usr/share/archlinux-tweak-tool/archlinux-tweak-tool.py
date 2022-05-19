#!/usr/bin/env python3

#      #============================================================
#      #= Authors: Brad Heffernan - Erik Dubois - Cameron Percival =
#      #============================================================

import Splash
import gi
import Functions
import pacman_functions
import Support
import Settings
import slim
import signal
import Gtk_Functions
import oblogout
import termite
import neofetch
import skelapp
import sddm
import lightdm
import themer
import desktopr
import autostart
import polybar
import zsh_theme
import fish
import distro
import user
import fixes
import GUI
import subprocess
import utilities
from Functions import os, pacman
from subprocess import PIPE, STDOUT
from time import sleep
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, Pango, GLib  # noqa

base_dir = os.path.dirname(os.path.realpath(__file__))
pmf = pacman_functions


class Main(Gtk.Window):
    def __init__(self):
        print("---------------------------------------------------------------------------")
        print("If you have errors, report it on the discord channel of ArcoLinux")
        print("If you have errors, because of SDDM and its cursor, user, theme, ...")
        print("Try running 'fix-sddm-conf' in a terminal")
        print("Then launch the Arch Linux Tweak Tool again")
        print("---------------------------------------------------------------------------")
        print("Created for :")
        print(" - ArcoLinux     - https://arcolinux.info")
        print(" - Arch Linux    - https://archlinux.org")
        print(" - Alci          - https://alci.online")
        print(" - Carli         - https://arcolinuxiso.com/")
        print(" - Ariser        - https://ariser.eu/")
        print(" - EndeavourOS   - https://endeavouros.com/")
        print(" - Garuda        - https://garudalinux.org/")
        print("---------------------------------------------------------------------------")
        print("Other Arch Linux based distros will be visited later")
        print("---------------------------------------------------------------------------")

        super(Main, self).__init__(title="Arch Linux Tweak Tool")
        self.set_border_width(10)
        self.connect("delete-event", self.on_close)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_icon_from_file(os.path.join(base_dir, 'images/archlinux.png'))
        self.set_default_size(800, 900)

        self.opened = True
        self.firstrun = True
        self.desktop = ""
        self.timeout_id = None

        self.desktop_status = Gtk.Label()
        self.image_DE = Gtk.Image()

        self.grub_image_path = ""
        self.fb = Gtk.FlowBox()

        splScr = Splash.splashScreen()

        while Gtk.events_pending():
            Gtk.main_iteration()

        t = Functions.threading.Thread(target=Functions.get_desktop,
                                       args=(self,))
        t.daemon = True
        t.start()
        t.join()

        #make backup of ~/.zshrc
        if os.path.isfile(Functions.zsh_config):
            if not os.path.isfile(Functions.zsh_config + ".bak"):
                Functions.shutil.copy(Functions.zsh_config, Functions.zsh_config + ".bak")
                Functions.permissions(Functions.home + "/.zshrc.bak")

        #make backup of /etc/default/grub
        if not os.path.isfile(Functions.grub_default_grub + ".bak"):
            Functions.shutil.copy(Functions.grub_default_grub, Functions.grub_default_grub + ".bak")

        #make backup of /etc/pacman.conf
        if not os.path.isfile(Functions.pacman + ".bak"):
            Functions.shutil.copy(Functions.pacman, Functions.pacman + ".bak")

        #make backup of .config/xfce4/terminal/terminalrc
        if Functions.file_check(Functions.xfce4_terminal_config):
            if not os.path.isfile(Functions.xfce4_terminal_config + ".bak"):
                Functions.shutil.copy(Functions.xfce4_terminal_config, Functions.xfce4_terminal_config + ".bak")
                Functions.permissions(Functions.xfce4_terminal_config + ".bak")

        #make backup of .config/alacritty/alacritty.yml
        if Functions.file_check(Functions.alacritty_config):
            if not os.path.isfile(Functions.alacritty_config + ".bak"):
                Functions.shutil.copy(Functions.alacritty_config, Functions.alacritty_config + ".bak")
                Functions.permissions(Functions.alacritty_config + ".bak")

        #make directory if it doesn't exist
        if not os.path.isdir(Functions.log_dir):
            try:
                os.mkdir(Functions.log_dir)
            except Exception as e:
                print(e)

        #make directory if it doesn't exist
        if not os.path.isdir(Functions.att_log_dir):
            try:
                os.mkdir(Functions.att_log_dir)
            except Exception as e:
                print(e)

        #make directory if it doesn't exist'
        if os.path.exists("/usr/bin/sddm"):
            if not os.path.isdir(Functions.sddm_default_d2_dir):
                try:
                    os.mkdir(Functions.sddm_default_d2_dir)
                except Exception as e:
                    print(e)

            #if there is an sddm.conf but is empty = 0
            if Functions.os.path.isfile(Functions.sddm_conf):
                if  os.path.getsize(Functions.sddm_conf) == 0:
                    Functions.shutil.copy(Functions.sddm_default_d_sddm_original_1,
                                        Functions.sddm_default_d1)
                    Functions.shutil.copy(Functions.sddm_default_d_sddm_original_2,
                                        Functions.sddm_default_d2)
            #if there is NO sddm.conf
            if not Functions.os.path.exists(Functions.sddm_conf):
                try:
                    Functions.shutil.copy(Functions.sddm_default_d_sddm_original_1,
                                          Functions.sddm_default_d1)
                    Functions.shutil.copy(Functions.sddm_default_d_sddm_original_2,
                                          Functions.sddm_default_d2)
                    Functions.restart_program()
                except OSError as e:
                    #This will ONLY execute if the sddm files and the underlying sddm files do not exist
                    if e.errno == 2:
                        command = '/usr/local/bin/arcolinux-fix-sddm-config'
                        Functions.subprocess.call(command,
                                        shell=True,
                                        stdout=Functions.subprocess.PIPE,
                                        stderr=Functions.subprocess.STDOUT)
                        print("The SDDM files in your installation either did not exist, or were corrupted.")
                        print("These files have now been restored. Please re-run the Tweak Tool if it did not load for you.")
                        Functions.restart_program()

        #adding lines to sddm
        if Functions.os.path.isfile(Functions.sddm_default_d2):
            session_exists = sddm.check_sddmk_session("Session=")
            if session_exists is False:
                sddm.insert_session("#Session=")

        #adding lines to sddm
        if Functions.os.path.isfile(Functions.sddm_default_d2):
            user_exists = sddm.check_sddmk_user("User=")
            if user_exists is False:
                sddm.insert_user("#User=")

        #ensuring we have a neofetch directory
        if not Functions.os.path.exists(Functions.home + "/.config/neofetch"):
            Functions.os.makedirs(Functions.home + "/.config/neofetch", 0o766)
            Functions.permissions(Functions.home + "/.config/neofetch")

        #ensuring we have a backup of current neofetch
        if os.path.isfile(Functions.neofetch_config):
            if not os.path.isfile(Functions.neofetch_config + ".bak"):
                Functions.shutil.copy(Functions.neofetch_config, Functions.neofetch_config + ".bak")
                Functions.permissions(Functions.neofetch_config + ".bak")

        #ensuring we have a neofetch config to start with
        if not os.path.isfile(Functions.neofetch_config):
            Functions.shutil.copy(Functions.neofetch_arco, Functions.neofetch_config)
            Functions.permissions(Functions.neofetch_config)

        #ensuring we have .autostart
        if not Functions.os.path.exists(Functions.home + "/.config/autostart"):
            Functions.os.makedirs(Functions.home + "/.config/autostart", 0o766)
            Functions.permissions(Functions.home + "/.config/autostart")

        #ensuring we have a directory for backups
        if not Functions.os.path.isdir(Functions.home + "/.config/archlinux-tweak-tool"):
            Functions.os.makedirs(Functions.home + "/.config/archlinux-tweak-tool", 0o766)
            Functions.permissions(Functions.home + "/.config/archlinux-tweak-tool")

        #ensuring permissions
        a1 = Functions.os.stat(Functions.home + "/.config/autostart")
        a2 = Functions.os.stat(Functions.home + "/.config/archlinux-tweak-tool")
        autostart = a1.st_uid
        att = a2.st_uid

        #fixing root permissions if the folder exists
        #can be removed later - 02/11/2021 startdate
        if os.path.exists(Functions.home + "/.config-att"):
            Functions.permissions(Functions.home + "/.config-att")

        if autostart == 0:
            Functions.permissions(Functions.home + "/.config/autostart")
            print("Fix autostart permissions...")

        if att == 0:
            Functions.permissions(Functions.home + "/.config/archlinux-tweak-tool")
            print("Fix archlinux-tweak-tool permissions...")

        # if not Functions.path_check(Functions.config_dir + "images"):
        #     Functions.os.makedirs(Functions.config_dir + "images", 0o766)
        #     for x in Functions.os.listdir(base_dir + "/polybar_data/"):
        #         Functions.copy_func(base_dir + "/polybar_data/" + x, Functions.config_dir + "images", False)
        #     Functions.permissions(Functions.config_dir + "images")
        # else:
        #     for x in Functions.os.listdir(base_dir + "/polybar_data/"):
        #         Functions.copy_func(base_dir + "/polybar_data/" + x, Functions.config_dir + "images", False)
        #     Functions.permissions(Functions.config_dir + "images")

        if not Functions.os.path.isfile(Functions.config):
            key = {"theme": ""}
            Settings.make_file("TERMITE", key)
            Functions.permissions(Functions.config)

        GUI.GUI(self, Gtk, Gdk, GdkPixbuf, base_dir, os, Pango)

#       #========================ARCO REPO=============================

        arco_testing = pmf.check_repo("[arcolinux_repo_testing]")
        arco_base = pmf.check_repo("[arcolinux_repo]")
        arco_3p = pmf.check_repo("[arcolinux_repo_3party]")
        arco_xl = pmf.check_repo("[arcolinux_repo_xlarge]")

#       #========================ARCH REPO=============================

        arch_testing = pmf.check_repo("[testing]")
        arch_core = pmf.check_repo("[core]")
        arch_extra = pmf.check_repo("[extra]")
        arch_community_testing = pmf.check_repo("[community-testing]")
        arch_community = pmf.check_repo("[community]")
        arch_multilib_testing = pmf.check_repo("[multilib-testing]")
        arch_multilib = pmf.check_repo("[multilib]")

#       #========================OTHER REPO=============================

        chaotics_repo = pmf.check_repo("[chaotic-aur]")
        endeavouros_repo = pmf.check_repo("[endeavouros]")
        nemesis_repo = pmf.check_repo("[nemesis_repo]")

#       #========================ARCO MIRROR=============================
        if os.path.isfile(Functions.arcolinux_mirrorlist):
            arco_mirror_seed = pmf.check_mirror("Server = https://ant.seedhost.eu/arcolinux/$repo/$arch")
            arco_mirror_gitlab = pmf.check_mirror("Server = https://gitlab.com/arcolinux/$repo/-/raw/main/$arch")
            arco_mirror_belnet = pmf.check_mirror("Server = https://ftp.belnet.be/arcolinux/$repo/$arch")
            arco_mirror_codeberg = pmf.check_mirror("Server = https://codeberg.org/arcolinux/$repo/media/branch/main/$arch")
            arco_mirror_funami = pmf.check_mirror("Server = https://mirror.funami.tech/arcolinux/$repo/$arch")
            arco_mirror_jingk = pmf.check_mirror("Server = https://mirror.jingk.ai/arcolinux/$repo/$arch")
            arco_mirror_aarnet = pmf.check_mirror("Server = https://mirror.aarnet.edu.au/pub/arcolinux/$repo/$arch")
            arco_mirror_github = pmf.check_mirror("Server = https://arcolinux.github.io/$repo/$arch")

#       #========================ARCO MIRROR SET TOGGLE=====================
        if os.path.isfile(Functions.arcolinux_mirrorlist):
            self.aseed_button.set_active(arco_mirror_seed)
            self.agitlab_button.set_active(arco_mirror_gitlab)
            self.abelnet_button.set_active(arco_mirror_belnet)
            self.afunami_button.set_active(arco_mirror_funami)
            self.ajingk_button.set_active(arco_mirror_jingk)
            self.acodeberg_button.set_active(arco_mirror_codeberg)
            self.aarnet_button.set_active(arco_mirror_aarnet)
            #self.agithub_button.set_active(arco_mirror_github)

#       #========================ARCO REPO SET TOGGLE=====================

        self.atestrepo_button.set_active(arco_testing)
        self.arepo_button.set_active(arco_base)
        self.a3prepo_button.set_active(arco_3p)
        self.axlrepo_button.set_active(arco_xl)

#       #========================ARCH LINUX REPO SET TOGGLE==================

        self.checkbutton2.set_active(arch_testing)
        self.checkbutton6.set_active(arch_core)
        self.checkbutton7.set_active(arch_extra)
        self.checkbutton4.set_active(arch_community_testing)
        self.checkbutton5.set_active(arch_community)
        self.checkbutton3.set_active(arch_multilib_testing)
        self.checkbutton8.set_active(arch_multilib)

#       #========================OTHER REPO SET TOGGLE==================

        self.chaotics_button.set_active(chaotics_repo)
        self.opened = False
        self.endeavouros_button.set_active(endeavouros_repo)
        self.opened = False
        self.nemesis_button.set_active(nemesis_repo)
        self.opened = False

#       #========================NEOFETCH LOLCAT TOGGLE===================

        shell = Functions.get_shell()

        if shell == "zsh" or shell == "bash":

    #       #========================TERMINAL UTILITIES TOGGLES========================
            #screenfetch
            self.screenfetch_lolcat.set_active(utilities.get_term_rc("screenfetch | lolcat"))
            self.screenfetch_util.set_active(utilities.get_term_rc("screenfetch"))
            #ufetch
            self.ufetch_lolcat.set_active(utilities.get_term_rc("ufetch | lolcat"))
            self.ufetch_util.set_active(utilities.get_term_rc("ufetch"))
            #ufetch-arco
            self.ufetch_arco_lolcat.set_active(utilities.get_term_rc("ufetch-arco | lolcat"))
            self.ufetch_arco_util.set_active(utilities.get_term_rc("ufetch-arco"))
            #pfetch
            self.pfetch_lolcat.set_active(utilities.get_term_rc("pfetch | lolcat"))
            self.pfetch_util.set_active(utilities.get_term_rc("pfetch"))
            #paleofetch
            self.paleofetch_lolcat.set_active(utilities.get_term_rc("paleofetch | lolcat"))
            self.paleofetch_util.set_active(utilities.get_term_rc("paleofetch"))
            #alsi
            self.alsi_lolcat.set_active(utilities.get_term_rc("alsi | lolcat"))
            self.alsi_util.set_active(utilities.get_term_rc("alsi"))
            #hfetch
            self.hfetch_lolcat.set_active(utilities.get_term_rc("hfetch | lolcat"))
            self.hfetch_util.set_active(utilities.get_term_rc("hfetch"))
            #sfetch
            self.sfetch_lolcat.set_active(utilities.get_term_rc("sfetch | lolcat"))
            self.sfetch_util.set_active(utilities.get_term_rc("sfetch"))
            #sysinfo
            self.sysinfo_lolcat.set_active(utilities.get_term_rc("sysinfo | lolcat"))
            self.sysinfo_util.set_active(utilities.get_term_rc("sysinfo"))
            #fetch
            self.fetch_lolcat.set_active(utilities.get_term_rc("fetch | lolcat"))
            self.fetch_util.set_active(utilities.get_term_rc("fetch"))
            #sysinfo-retro
            self.sysinfo_retro_lolcat.set_active(utilities.get_term_rc("sysinfo-retro | lolcat"))
            self.sysinfo_retro_util.set_active(utilities.get_term_rc("sysinfo-retro"))
            #cpufetch
            self.cpufetch_lolcat.set_active(utilities.get_term_rc("cpufetch | lolcat"))
            self.cpufetch_util.set_active(utilities.get_term_rc("cpufetch"))
            #colorscripts
            self.colorscript.set_active(utilities.get_term_rc("colorscript random"))

            #Neofetch
            self.neo_lolcat.set_active(utilities.get_term_rc("neofetch | lolcat"))
            self.neofetch_lolcat.set_active(utilities.get_term_rc("neofetch | lolcat"))
            self.neofetch_util.set_active(utilities.get_term_rc("neofetch"))
            self.neo_util.set_active(utilities.get_term_rc("neofetch"))

        splScr.destroy()

        if Functions.os.path.isfile(Functions.lightdm_conf):
            if "#" in lightdm.check_lightdm(lightdm.get_lines(Functions.lightdm_conf),"autologin-user="):
                self.autologin.set_active(False)
                self.sessions.set_sensitive(False)
            else:
                self.autologin.set_active(True)
                self.sessions.set_sensitive(True)

        if os.path.exists("/usr/bin/sddm"):
            try:
                if not "plasma" in self.desktop.lower():
                    if sddm.check_sddm(sddm.get_sddm_lines(Functions.sddm_default_d1),"CursorTheme=") and sddm.check_sddm(sddm.get_sddm_lines(Functions.sddm_default_d2),"User="):
                        if Functions.os.path.isfile(Functions.sddm_default_d2):
                            if "#" in sddm.check_sddm(sddm.get_sddm_lines(Functions.sddm_default_d2),"User="):
                                self.autologin_sddm.set_active(False)
                                self.sessions_sddm.set_sensitive(False)
                            else:
                                self.autologin_sddm.set_active(True)
                                self.sessions_sddm.set_sensitive(True)
                        if Functions.os.path.isfile(Functions.sddm_default_d1):
                            read_cursor_name=sddm.check_sddm(sddm.get_sddm_lines(Functions.sddm_default_d1),"CursorTheme=").split("=")[1]
                            self.entry_cursor_name.set_text(read_cursor_name)
            except Exception as e:
                print(e)
                print("Run 'fix-sddm-conf' in a terminal")
                print("We will make backups of /etc/sddm.conf and /etc/sddm.conf.d/kde_settings.conf")

        if not os.path.isfile("/tmp/att.lock"):
            with open("/tmp/att.lock", "w") as f:
                f.write("")

    def on_close(self, widget, data):
        os.unlink("/tmp/att.lock")
        Gtk.main_quit()

    def create_autostart_columns(self, treeView):
        rendererText = Gtk.CellRendererText()
        renderer_checkbox = Gtk.CellRendererToggle()
        column_checkbox = Gtk.TreeViewColumn("", renderer_checkbox, active=0)
        renderer_checkbox.connect("toggled", self.renderer_checkbox, self.startups)
        renderer_checkbox.set_activatable(True)
        column_checkbox.set_sort_column_id(0)

        column = Gtk.TreeViewColumn("Name", rendererText, text=1)
        column.set_sort_column_id(1)

        column2 = Gtk.TreeViewColumn("Comment", rendererText, text=2)
        column2.set_sort_column_id(2)

        treeView.append_column(column_checkbox)
        treeView.append_column(column)
        treeView.append_column(column2)

    def create_columns(self, treeView):
        rendererText = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Name", rendererText, text=0)
        column.set_sort_column_id(0)
        treeView.append_column(column)

    def renderer_checkbox(self, renderer, path, model):
        if path is not None:
            it = model.get_iter(path)
            model[it][0] = not model[it][0]

    def on_activated(self, treeview, path, column):
        failed = False
        treestore, selected_treepaths = treeview.get_selection().get_selected_rows()
        selected_treepath = selected_treepaths[0]
        selected_row = treestore[selected_treepath]
        bool = selected_row[0]
        text = selected_row[1]

        if bool:
            bools = False
        else:
            bools = True

        with open(Functions.home + "/.config/autostart/" + text + ".desktop", "r") as f:
            lines = f.readlines()
            f.close()
        try:
            pos = Functions._get_position(lines, "Hidden=")
        except:
            failed = True
            with open(Functions.home + "/.config/autostart/" + text + ".desktop", "a") as f:
                f.write("Hidden=" + str(bools))
                f.close()
        if not failed:
            val = lines[pos].split("=")[1].strip()
            lines[pos] = lines[pos].replace(val, str(bools).lower())
            with open(Functions.home + "/.config/autostart/" + text + ".desktop", "w") as f:
                f.writelines(lines)
                f.close()

# =====================================================
#               PATREON LINK
# =====================================================

    def on_social_clicked(self, widget, event):
        sup = Support.Support(self)
        response = sup.run()

        if response == Gtk.ResponseType.DELETE_EVENT:
            sup.destroy()

    def tooltip_callback(self, widget, x, y, keyboard_mode, tooltip, text):
        tooltip.set_text(text)
        return True

# =====================================================
#               PACMAN FUNCTIONS
# =====================================================

    def on_mirror_seed_repo_toggle(self, widget, active):
        if not pmf.mirror_exist("Server = https://ant.seedhost.eu/arcolinux/$repo/$arch"):
            pmf.append_mirror(self, Functions.seedhostmirror)
        else:
            if self.opened is False:
                pmf.toggle_mirrorlist(self, widget.get_active(),
                                      "arco_mirror_seed")

    def on_mirror_gitlab_repo_toggle(self, widget, active):
        if not pmf.mirror_exist("Server = https://gitlab.com/arcolinux/$repo/-/raw/main/$arch"):
            pmf.append_mirror(self, Functions.seedhostmirror)
        else:
            if self.opened is False:
                pmf.toggle_mirrorlist(self, widget.get_active(),
                                      "arco_mirror_gitlab")

    def on_mirror_belnet_repo_toggle(self, widget, active):
        if not pmf.mirror_exist("Server = https://ant.seedhost.eu/arcolinux/$repo/$arch"):
            pmf.append_mirror(self, Functions.seedhostmirror)
        else:
            if self.opened is False:
                pmf.toggle_mirrorlist(self, widget.get_active(),
                                      "arco_mirror_belnet")

    def on_mirror_funami_repo_toggle(self, widget, active):
        if not pmf.mirror_exist("Server = https://mirror.funami.tech/arcolinux/$repo/$arch"):
            pmf.append_mirror(self, Functions.seedhostmirror)
        else:
            if self.opened is False:
                pmf.toggle_mirrorlist(self, widget.get_active(),
                                      "arco_mirror_funami")

    def on_mirror_jingk_repo_toggle(self, widget, active):
        if not pmf.mirror_exist("Server = https://mirror.jingk.ai/arcolinux/$repo/$arch"):
            pmf.append_mirror(self, Functions.seedhostmirror)
        else:
            if self.opened is False:
                pmf.toggle_mirrorlist(self, widget.get_active(),
                                      "arco_mirror_jingk")

    def on_mirror_codeberg_repo_toggle(self, widget, active):
        if not pmf.mirror_exist("Server = https://codeberg.org/arcolinux/$repo/media/branch/main/$arch"):
            pmf.append_mirror(self, Functions.seedhostmirror)
        else:
            if self.opened is False:
                pmf.toggle_mirrorlist(self, widget.get_active(),
                                      "arco_mirror_codeberg")

    def on_mirror_aarnet_repo_toggle(self, widget, active):
        if not pmf.mirror_exist("Server = https://mirror.aarnet.edu.au/pub/arcolinux/$repo/$arch"):
            pmf.append_mirror(self, Functions.aarnetmirror)
        else:
            if self.opened is False:
                pmf.toggle_mirrorlist(self, widget.get_active(), "arco_mirror_aarnet")

    def on_mirror_github_repo_toggle(self, widget, active):
        if not pmf.mirror_exist("Server = https://ant.seedhost.eu/arcolinux/$repo/$arch"):
            pmf.append_mirror(self, Functions.seedhostmirror)
        else:
            if self.opened is False:
                pmf.toggle_mirrorlist(self, widget.get_active(),
                                      "arco_mirror_github")
    def on_pacman_atestrepo_toggle(self, widget, active):
        if not pmf.repo_exist("[arcolinux_repo_testing]"):
            pmf.append_repo(self, Functions.atestrepo)
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(),
                                      "arco_testing")

    def on_pacman_arepo_toggle(self, widget, active):
        if not pmf.repo_exist("[arcolinux_repo]"):
            pmf.append_repo(self, Functions.arepo)
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(),
                                      "arco_base")

    def on_pacman_a3p_toggle(self, widget, active):
        if not pmf.repo_exist("[arcolinux_repo_3party]"):
            pmf.append_repo(self, Functions.a3drepo)
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(),
                                      "arco_a3p")

    def on_pacman_axl_toggle(self, widget, active):
        if not pmf.repo_exist("[arcolinux_repo_xlarge]"):
            pmf.append_repo(self, Functions.axlrepo)
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(),
                                      "arco_axl")

    def on_chaotics_toggle(self, widget, active):
        if not pmf.repo_exist("[chaotic-aur]"):
            pmf.append_repo(self, Functions.chaotics_repo)
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(),
                                      "chaotics")

    def on_endeavouros_toggle(self, widget, active):
        if not pmf.repo_exist("[endeavouros]"):
            pmf.append_repo(self, Functions.endeavouros_repo)
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(),
                                      "endeavouros")

    def on_nemesis_toggle(self, widget, active):
        if not pmf.repo_exist("[nemesis_repo]"):
            pmf.append_repo(self, Functions.nemesis_repo)
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(),
                                      "nemesis")

    def on_pacman_toggle1(self, widget, active):
        if not pmf.repo_exist("[testing]"):
            pmf.append_repo(self, Functions.arch_testing_repo)
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(),
                                      "testing")

    def on_pacman_toggle2(self, widget, active):
        if not pmf.repo_exist("[core]"):
            pmf.append_repo(self, Functions.arch_core_repo)
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(),
                                      "core")

    def on_pacman_toggle3(self, widget, active):
        if not pmf.repo_exist("[extra]"):
            pmf.append_repo(self, Functions.arch_extra_repo)
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(),
                                      "extra")

    def on_pacman_toggle4(self, widget, active):
        if not pmf.repo_exist("[community-testing]"):
            pmf.append_repo(self, Functions.arch_community_testing_repo)
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(),
                                      "community-testing")

    def on_pacman_toggle5(self, widget, active):
        if not pmf.repo_exist("[community]"):
            pmf.append_repo(self, Functions.arch_community_repo)
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(),
                                      "community")

    def on_pacman_toggle6(self, widget, active):
        if not pmf.repo_exist("[multilib-testing]"):
            pmf.append_repo(self, Functions.arch_multilib_testing_repo)
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(),
                                      "multilib-testing")

    def on_pacman_toggle7(self, widget, active):
        if not pmf.repo_exist("[multilib]"):
            pmf.append_repo(self, Functions.arch_multilib_repo)
        else:
            if self.opened is False:
                pmf.toggle_test_repos(self, widget.get_active(),
                                      "multilib")

    def button1_clicked(self, widget):
        self.text = self.textbox1.get_buffer()
        startiter, enditer = self.text.get_bounds()

        if not len(self.text.get_text(startiter, enditer, True)) < 5:
            print(self.text.get_text(startiter, enditer, True))
            pmf.append_repo(
                self, self.text.get_text(startiter, enditer, True))

    # =====================================================
    #               THEMER FUNCTIONS
    # =====================================================

    def on_polybar_toggle(self, widget, active):
        if widget.get_active():
            themer.toggle_polybar(self, themer.get_list(Functions.i3wm_config), True)
        else:
            themer.toggle_polybar(self, themer.get_list(Functions.i3wm_config), False)
            Functions.subprocess.run(["killall", "-q", "polybar"], shell=False)

    def awesome_apply_clicked(self, widget):
        if not os.path.isfile(Functions.awesome_config + ".bak"):
            Functions.shutil.copy(Functions.awesome_config,
                                  Functions.awesome_config + ".bak")

        tree_iter = self.awesome_combo.get_active_iter()
        if tree_iter is not None:
            model = self.awesome_combo.get_model()
            row_id, name = model[tree_iter][:2]
        nid = str(row_id+1)
        themer.set_awesome_theme(themer.get_list(Functions.awesome_config),
                                 nid)
        Functions.show_in_app_notification(self, "Theme set successfully")

    def awesome_reset_clicked(self, widget):
        if os.path.isfile(Functions.awesome_config + ".bak"):
            Functions.shutil.copy(Functions.awesome_config + ".bak",
                                  Functions.awesome_config)
            Functions.show_in_app_notification(self,
                                               "Config reset successfully")

            awesome_list = themer.get_list(Functions.awesome_config)
            awesome_lines = themer.get_awesome_themes(awesome_list)

            self.store.clear()
            for x in range(len(awesome_lines)):
                self.store.append([x, awesome_lines[x]])
            val = int(themer.get_value(awesome_list, "local chosen_theme =")
                      .replace("themes[", "").replace("]", ""))
            self.awesome_combo.set_active(val-1)

    def i3wm_apply_clicked(self, widget):
        if os.path.isfile(Functions.i3wm_config):
            Functions.shutil.copy(Functions.i3wm_config,
                                  Functions.i3wm_config + ".bak")

        themer.set_i3_themes(themer.get_list(Functions.i3wm_config),
                             self.i3_combo.get_active_text())
        if not themer.check_polybar(themer.get_list(Functions.i3wm_config)):
            themer.set_i3_themes_bar(themer.get_list(Functions.i3wm_config),
                                     self.i3_combo.get_active_text())
        Functions.show_in_app_notification(self,
                                           "Theme applied successfully")

    def i3wm_reset_clicked(self, widget):
        if os.path.isfile(Functions.i3wm_config + ".bak"):
            Functions.shutil.copy(Functions.i3wm_config + ".bak",
                                  Functions.i3wm_config)
            Functions.show_in_app_notification(self,
                                               "Config reset successfully")

            i3_list = themer.get_list(Functions.i3wm_config)

            themer.get_i3_themes(self.i3_combo, i3_list)

    def qtile_apply_clicked(self, widget):
        if os.path.isfile(Functions.qtile_config):
            Functions.shutil.copy(Functions.qtile_config,
                                  Functions.qtile_config + ".bak")

        themer.set_qtile_themes(themer.get_list(Functions.qtile_config),
                             self.qtile_combo.get_active_text())
        Functions.show_in_app_notification(self,
                                           "Theme applied successfully")

    def qtile_reset_clicked(self, widget):
        if os.path.isfile(Functions.qtile_config + ".bak"):
            Functions.shutil.copy(Functions.qtile_config + ".bak",
                                  Functions.qtile_config)
            Functions.show_in_app_notification(self,
                                               "Config reset successfully")

            qtile_list = themer.get_list(Functions.qtile_config)

            themer.get_qtile_themes(self.qtile_combo, qtile_list)

    # =====================================================
    #               OBLOGOUT FUNCTIONS
    # =====================================================

    def save_oblogout(self, widget):  # noqa
        # widget.set_sensitive(False)
        if not os.path.isfile(Functions.oblogout_conf + ".bak"):
            Functions.shutil.copy(Functions.oblogout_conf,
                                  Functions.oblogout_conf + ".bak")
        try:
            string = ""
            if self.check_cancel.get_active():
                string += "cancel "
            if self.check_logout.get_active():
                string += "logout "
            if self.check_restart.get_active():
                string += "restart "
            if self.check_shut.get_active():
                string += "shutdown "
            if self.check_susp.get_active():
                string += "suspend "
            if self.check_hiber.get_active():
                string += "hibernate "
            if self.check_lock.get_active():
                string += "lock "

            oblogout.set_buttons(self, string.strip().replace(" ", ", "))
            oblogout.oblogout_change_theme(self, self.oblog.get_active_text())
            oblogout.set_opacity(self, self.hscale.get_value())
            # oblogout.set_command(self, "lock", self.lockBox.get_text())
            oblogout.set_shorcut(self,
                                 "shutdown",
                                 self.tbshutdown.get_text().capitalize())
            oblogout.set_shorcut(self,
                                 "restart",
                                 self.tbrestart.get_text().capitalize())
            oblogout.set_shorcut(self,
                                 "suspend",
                                 self.tbsuspend.get_text().capitalize())
            oblogout.set_shorcut(self,
                                 "logout",
                                 self.tblogout.get_text().capitalize())
            oblogout.set_shorcut(self,
                                 "cancel",
                                 self.tbcancel.get_text().capitalize())
            oblogout.set_shorcut(self,
                                 "hibernate",
                                 self.tbhibernate.get_text().capitalize())
            oblogout.set_shorcut(self,
                                 "lock",
                                 self.tblock.get_text().capitalize())
            # hex = Functions.rgb_to_hex(
            #     self.colorchooser.get_rgba().to_string())
            # oblogout.set_color(self, hex.upper())

            Functions.show_in_app_notification(self,
                                               "Settings Saved Successfully")
        except Exception as e:
            print(e)

    # =====================================================
    #               Gtk FUNCTIONS
    # =====================================================

    def save_gtk3_settings(self,
                           widget,
                           themeCombo,
                           iconCombo,
                           cursorCombo,
                           cursor_size):
        widget.set_sensitive(False)

        t = Functions.threading.Thread(target=Gtk_Functions.gtk_settings_saved,
                                       args=(self,
                                             themeCombo.get_active_text(),
                                             iconCombo.get_active_text(),
                                             cursorCombo.get_active_text(),
                                             int(str(cursor_size.get_value()
                                                     ).split(".")[0])))
        t.daemon = True
        t.start()

        Functions.show_in_app_notification(self, "Settings Saved Successfully")
        widget.set_sensitive(True)

    def blank_pacman(source,target):
        Functions.shutil.copy(Functions.pacman,
                                  Functions.pacman + ".bak")
        if distro.id() == "arch":
            Functions.shutil.copy(Functions.blank_pacman_arch, Functions.pacman)
        if distro.id() == "arcolinux":
            Functions.shutil.copy(Functions.blank_pacman_arco, Functions.pacman)
        if distro.id() == "endeavouros":
            Functions.shutil.copy(Functions.blank_pacman_eos, Functions.pacman)
        if distro.id() == "garuda":
            Functions.shutil.copy(Functions.blank_pacman_garuda, Functions.pacman)

    def reset_pacman_local(self, widget):  # noqa
        if os.path.isfile(Functions.pacman + ".bak"):
            Functions.shutil.copy(Functions.pacman + ".bak", Functions.pacman)
            print("We have used /etc/pacman.conf.bak to reset /etc/pacman.conf")
            Functions.show_in_app_notification(self,
                                               "Default Settings Applied")

    def reset_pacman_online(self,widget): # noqa
        if distro.id() == "arch":
            Functions.shutil.copy(Functions.pacman_arch, Functions.pacman)
        if distro.id() == "arcolinux":
            Functions.shutil.copy(Functions.pacman_arco, Functions.pacman)
        if distro.id() == "endeavouros":
            Functions.shutil.copy(Functions.pacman_eos, Functions.pacman)
        if distro.id() == "garuda":
            Functions.shutil.copy(Functions.pacman_garuda, Functions.pacman)
        print("The online version of /etc/pacman.conf is saved")
        Functions.show_in_app_notification(self,
                                            "Default Settings Applied")
        # elif filez == Functions.gtk3_settings:

        #     if os.path.isfile(Functions.gtk2_settings + ".bak"):
        #         Functions.shutil.copy(Functions.gtk2_settings + ".bak",
        #                               Functions.gtk2_settings)

        #     if os.path.isfile(Functions.xfce_config + ".bak"):
        #         Functions.shutil.copy(Functions.xfce_config + ".bak",
        #                               Functions.xfce_config)

        #     Gtk_Functions.get_gtk_themes(self, self.themeCombo)
        #     Gtk_Functions.get_icon_themes(self, self.iconCombo)
        #     Gtk_Functions.get_cursor_themes(self, self.cursorCombo)

        #     self.cursor_size.set_value(
        #         float(Gtk_Functions.get_gtk_settings("gtk-cursor-theme-size")))
            # self.fonts.set_font(
            #     Gtk_Functions.get_gtk_settings("gtk-font-name"))
            # Functions.subprocess.call(["xsetroot -xcf /usr/share/icons/" +
            #                            self.cursorCombo.get_active_text() +
            #                            "/cursors/left_ptr " +
            #                            str(self.cursor_size.get_value())],
            #                           shell=True)
            # Functions.show_in_app_notification(self,
            #                                    "Default Settings Applied")
        # elif filez == Functions.oblogout_conf:
        #     self.oblog.get_model().clear()
        #     vals = oblogout.get_opacity()
        #     self.hscale.set_value(vals)
        #     try:
        #         self.tbcancel.set_text(oblogout.get_shortcut("cancel"))
        #         self.tbshutdown.set_text(oblogout.get_shortcut("shutdown"))
        #         self.tbsuspend.set_text(oblogout.get_shortcut("suspend"))
        #         self.tbrestart.set_text(oblogout.get_shortcut("restart"))
        #         self.tblogout.set_text(oblogout.get_shortcut("logout"))
        #         self.tbhibernate.set_text(oblogout.get_shortcut("hibernate"))
        #         self.tblock.set_text(oblogout.get_shortcut("lock"))
        #     except Exception as e:
        #         print(e)
            # self.lockBox.set_text(oblogout.get_command("lock"))
            # color = Gdk.RGBA()
            # color.parse(oblogout.get_color())
            # self.colorchooser.set_rgba(color)
            # btnString = oblogout.get_buttons()
            # oblogout.oblog_populate(self.oblog)

            # if "shutdown" in btnString:
            #     self.check_shut.set_active(True)
            # if "lock" in btnString:
            #     self.check_lock.set_active(True)
            # if "logout" in btnString:
            #     self.check_logout.set_active(True)
            # if "restart" in btnString:
            #     self.check_restart.set_active(True)
            # if "cancel" in btnString:
            #     self.check_cancel.set_active(True)
            # if "suspend" in btnString:
            #     self.check_susp.set_active(True)
            # if "hibernate" in btnString:
            #     self.check_hiber.set_active(True)
            # Functions.show_in_app_notification(self,
            #                                    "Default Settings Applied")

    #   #====================================================================
    #   #                       HBLOCK SECURITY PRIVACY
    #   #====================================================================

    def set_hblock(self, widget, state):
        if self.firstrun is not True:
            t = Functions.threading.Thread(target=Functions.set_hblock, args=(
                self, widget, widget.get_active()))
            t.start()
        else:
            self.firstrun = False

    def set_ublock_firefox(self, widget, state):
        t = Functions.threading.Thread(target=Functions.set_firefox_ublock, args=(
                self, widget, widget.get_active()))
        t.start()

    #   #====================================================================
    #   #                       GRUB
    #   #====================================================================

    def on_grub_item_clicked(self, widget, data):
        for x in data:
            self.grub_image_path = x.get_name()

    def on_set_grub_wallpaper(self, widget):
        if not os.path.isfile(Functions.grub_theme_conf):
            self.on_click_install_arco_vimix_clicked(self)

        if self.grub_image_path == "":
            Functions.show_in_app_notification(self, "First choose a wallpaper image")
        else:
            Functions.set_grub_wallpaper(self,
                                     self.grub_image_path)

    def on_reset_grub_wallpaper(self, widget):
        if os.path.isfile(Functions.grub_theme_conf + ".bak"):
            Functions.shutil.copy(Functions.grub_theme_conf + ".bak",
                                  Functions.grub_theme_conf)
        self.pop_themes_grub(self.grub_theme_combo,
                             Functions.get_grub_wallpapers(), True)

        if not os.path.isfile(Functions.grub_theme_conf):
            self.on_click_install_arco_vimix_clicked(self)

        print("Default Vimix grub wallpaper applied")
        Functions.show_in_app_notification(self, "Default Vimix grub wallpaper applied")

    def on_reset_grub(self, widget):
        if os.path.isfile(Functions.grub_default_grub + ".bak"):
            Functions.shutil.copy(Functions.grub_default_grub + ".bak",
                                  Functions.grub_default_grub)
        self.pop_themes_grub(self.grub_theme_combo,
                             Functions.get_grub_wallpapers(), True)

        print("/etc/default/grub.bak is used to reset your grub")
        Functions.show_in_app_notification(self, "Default Grub applied")

        command = 'grub-mkconfig -o /boot/grub/grub.cfg'
        Functions.subprocess.call(command.split(" "),
                        shell=False,
                        stdout=Functions.subprocess.PIPE,
                        stderr=Functions.subprocess.STDOUT)
        print("We have updated your grub with 'sudo grub-mkconfig -o /boot/grub/grub.cfg'")
        GLib.idle_add(Functions.show_in_app_notification, self, "Your original grub file has been applied")

    def pop_themes_grub(self, combo, lists, start):
        if os.path.isfile(Functions.grub_theme_conf):
            combo.get_model().clear()
            with open(Functions.grub_theme_conf, "r") as f:
                listss = f.readlines()
                f.close()

            val = Functions._get_position(listss, "desktop-image: ")
            bg_image = listss[val].split(" ")[1].replace("\"", "").strip()

            for x in self.fb.get_children():
                self.fb.remove(x)

            for x in lists:
                pb = GdkPixbuf.Pixbuf().new_from_file_at_size("/boot/grub/themes/Vimix/" + x, 128, 128) # noqa
                pimage = Gtk.Image()
                pimage.set_name("/boot/grub/themes/Vimix/" + x)
                pimage.set_from_pixbuf(pb)
                self.fb.add(pimage)
                pimage.show_all()

    def on_grub_theme_change(self, widget):
        try:
            pixbuf3 = GdkPixbuf.Pixbuf().new_from_file_at_size('/boot/grub/themes/Vimix/' +  # noqa
                                                               widget.get_active_text(),  # noqa
                                                               645, 645)
            print(widget.get_active_text())
            self.image_grub.set_from_pixbuf(pixbuf3)
        except Exception as e:
            print(e)

    def on_import_wallpaper(self, widget):
        text = self.tbimage.get_text()
        if len(text) > 1:
            print(os.path.basename(text))
            Functions.shutil.copy(text, '/boot/grub/themes/Vimix/' +
                                  os.path.basename(text))
            self.pop_themes_grub(self.grub_theme_combo,
                                 Functions.get_grub_wallpapers(), False)

    def on_remove_wallpaper(self, widget):
        widget.set_sensitive(False)
        if os.path.isfile(self.grub_image_path):

        # if os.path.isfile('/boot/grub/themes/Vimix/' +
        #                   self.grub_theme_combo.get_active_text()):
            excludes = ["archlinux03.jpg", "archlinux04.jpg",
                        "archlinux06.jpg", "archlinux07.jpg",
                        "arcolinux01.jpg", "arcolinux02.jpg",
                        "arcolinux03.jpg", "arcolinux04.jpg",
                        "arcolinux05.jpg", "arcolinux06.jpg",
                        "arcolinux07.jpg", "arcolinux08.jpg",
                        "background-slaze.jpg", "background-stylish.jpg",
                        "background-tela.jpg", "background-vimix.jpg",
                        "archlinux01.png",
                        "archlinux02.png", "archlinux05.png",
                        "arcolinux09.png",
                        "arcolinux10.png", "arcolinux11.png", "arcolinux.png",
                        "background.png"]

            # if not self.grub_theme_combo.get_active_text() in excludes:
            if not Functions.os.path.basename(self.grub_image_path) in excludes:
                # os.unlink('/boot/grub/themes/Vimix/' +
                #           self.grub_theme_combo.get_active_text())
                os.unlink(self.grub_image_path)
                self.pop_themes_grub(self.grub_theme_combo,
                                     Functions.get_grub_wallpapers(),
                                     True)
                Functions.show_in_app_notification(self,
                                                   "Wallpaper removed successfully")  # noqa
            else:
                Functions.show_in_app_notification(self,
                                                   "You can not remove that wallpaper")  # noqa
        widget.set_sensitive(True)

    def on_choose_wallpaper(self, widget):
        dialog = Gtk.FileChooserDialog(
                                       title="Please choose a file",
                                       action=Gtk.FileChooserAction.OPEN,)
        filter = Gtk.FileFilter()
        filter.set_name("IMAGE Files")
        filter.add_mime_type("image/png")
        filter.add_mime_type("image/jpg")
        filter.add_mime_type("image/jpeg")
        dialog.set_filter(filter)
        dialog.set_current_folder(Functions.home)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Open",
                           Gtk.ResponseType.OK)
        dialog.connect("response", self.open_response_cb)

        dialog.show()

    def open_response_cb(self, dialog, response):
        if response == Gtk.ResponseType.OK:
            self.tbimage.set_text(dialog.get_filename())
            dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()

    def on_click_install_arco_vimix_clicked(self, desktop):
        command = 'pacman -S arcolinux-grub-theme-vimix-git --noconfirm'
        Functions.subprocess.call(command.split(" "),
                        shell=False,
                        stdout=Functions.subprocess.PIPE,
                        stderr=Functions.subprocess.STDOUT)
        print("arcolinux-grub-theme-vimix-git has been installed")

        #changing /etc/default/grub to vimix theme
        Functions.set_default_theme(self)

        command = 'grub-mkconfig -o /boot/grub/grub.cfg'
        Functions.subprocess.call(command.split(" "),
                        shell=False,
                        stdout=Functions.subprocess.PIPE,
                        stderr=Functions.subprocess.STDOUT)
        print("We have updated your grub with 'sudo grub-mkconfig -o /boot/grub/grub.cfg'")
        GLib.idle_add(Functions.show_in_app_notification, self, "Setting saved successfully")
        Functions.restart_program()

    def on_reset_grub_vimix(self, desktop):
        command = 'pacman -S arcolinux-grub-theme-vimix-git --noconfirm'
        Functions.subprocess.call(command.split(" "),
                        shell=False,
                        stdout=Functions.subprocess.PIPE,
                        stderr=Functions.subprocess.STDOUT)
        print("arcolinux-grub-theme-vimix-git has been installed")

        #changing /etc/default/grub to vimix theme
        Functions.set_default_theme(self)

        command = 'grub-mkconfig -o /boot/grub/grub.cfg'
        Functions.subprocess.call(command.split(" "),
                        shell=False,
                        stdout=Functions.subprocess.PIPE,
                        stderr=Functions.subprocess.STDOUT)
        print("We have updated your grub with 'sudo grub-mkconfig -o /boot/grub/grub.cfg'")
        GLib.idle_add(Functions.show_in_app_notification, self, "Vimix has been installed")


    #    #====================================================================
    #    #                       SLIMLOCK
    #    #====================================================================

    def on_slim_apply(self, widget):
        if not os.path.isfile(Functions.slimlock_conf + ".bak"):
            Functions.shutil.copy(Functions.slimlock_conf,
                                  Functions.slimlock_conf + ".bak")
        slim.set_slimlock(self, self.slimbox.get_active_text())

    def on_slim_reset(self, widget):
        if os.path.isfile(Functions.slimlock_conf + ".bak"):
            Functions.shutil.copy(Functions.slimlock_conf + ".bak",
                                  Functions.slimlock_conf)
        slim.get_slimlock(self.slimbox)
        Functions.show_in_app_notification(self, "Default Settings Applied")

    def on_slim_theme_change(self, widget, image):
        try:
            path = '/usr/share/slim/themes/' + widget.get_active_text()
            pixbuf4 = GdkPixbuf.Pixbuf().new_from_file_at_size(path + "/background.png", 345, 345)  # noqa
            self.image2.set_from_pixbuf(pixbuf4)
        except Exception as e:
            print(e)

    def on_browser_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(
                                       title="Please choose a file",
                                       action=Gtk.FileChooserAction.OPEN,)
        filter = Gtk.FileFilter()
        filter.set_name("IMAGE Files")
        filter.add_mime_type("image/png")
        dialog.set_filter(filter)
        dialog.set_current_folder(Functions.home)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Open",
                           Gtk.ResponseType.OK)
        dialog.connect("response", self.open_response_slim)

        dialog.show()

    def open_response_slim(self, dialog, response):
        if response == Gtk.ResponseType.OK:
            self.slimtext.set_text(dialog.get_filename())
            pixbuf4 = GdkPixbuf.Pixbuf().new_from_file_at_size(self.slimtext.get_text(), 345, 345)  # noqa
            self.image5.set_from_pixbuf(pixbuf4)
            dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()

    def on_create_theme_clicked(self, widget):
        path = "/usr/share/slim/themes/"
        if os.path.isdir(path):
            if len(self.slimtheme.get_text()) >= 3 and len(self.slimtext.get_text()) > 3:  # noqa
                try:
                    os.mkdir(path + self.slimtheme.get_text())
                except Exception as e:
                    print(e)

                Functions.shutil.copy(base_dir + "/slim_data/info.txt",
                                      path + self.slimtheme.get_text() +
                                      "/info.txt")
                Functions.shutil.copy(base_dir + "/slim_data/panel.png",
                                      path + self.slimtheme.get_text() +
                                      "/panel.png")
                Functions.shutil.copy(base_dir + "/slim_data/slim.theme",
                                      path + self.slimtheme.get_text() +
                                      "/slim.theme")
                Functions.shutil.copy(self.slimtext.get_text(),
                                      path + self.slimtheme.get_text() +
                                      "/background.png")

                slim.reload_import(self.slimbox, self.slimtheme.get_text())
                self.image5.set_from_pixbuf(None)
                Functions.show_in_app_notification(self,
                                                   "Theme imported successfully")  # noqa

    def on_remove_theme(self, widget):
        path = "/usr/share/slim/themes/"
        try:
            if "arcolinux" not in self.slimbox.get_active_text():
                Functions.shutil.rmtree(path + self.slimbox.get_active_text())
                slim.remove_theme(self.slimbox.get_active_text())
                slim.reload_import(self.slimbox, "arcolinux_eyes")
                Functions.show_in_app_notification(self,
                                                   "Settings Saved Successfully")  # noqa
            else:
                Functions.show_in_app_notification(self,
                                                   "You can not remove that theme")  # noqa
        except Exception as e:
            print(e)

    #    #====================================================================
    #    #                       TERMINALS
    #    #====================================================================

    def on_clicked_install_alacritty_themes(self,widget):
        command = 'pacman -S alacritty ttf-hack arcolinux-alacritty-git alacritty-themes base16-alacritty-git --needed --noconfirm'
        Functions.subprocess.call(command.split(" "),
                        shell=False,
                        stdout=Functions.subprocess.PIPE,
                        stderr=Functions.subprocess.STDOUT)
        print("Installing alacritty ttf-hack arcolinux-alacritty-git alacritty-themes base16-alacritty-git ")
        GLib.idle_add(Functions.show_in_app_notification, self, "Alacritty Themes Installed")

        #if there is no file copy/paste from /etc/skel else alacritty-themes crash
        if not os.path.isfile(Functions.alacritty_config):
            if not os.path.isdir(Functions.alacritty_config_dir):
                try:
                    os.mkdir(Functions.alacritty_config_dir)
                except Exception as e:
                    print(e)

            Functions.shutil.copy(Functions.alacritty_arco,
                                  Functions.alacritty_config)
            Functions.permissions(Functions.home + "/.config/alacritty")
            print("Alacritty config saved")

    def on_clicked_install_xfce4_themes(self,widget):
        command = 'pacman -S xfce4-terminal-base16-colors-git xfce4-terminal tempus-themes-xfce4-terminal-git prot16-xfce4-terminal --needed --noconfirm'
        Functions.subprocess.call(command.split(" "),
                        shell=False,
                        stdout=Functions.subprocess.PIPE,
                        stderr=Functions.subprocess.STDOUT)
        print("Installing xfce4-terminal-base16-colors-git xfce4-terminal tempus-themes-xfce4-terminal-git prot16-xfce4-terminal")
        GLib.idle_add(Functions.show_in_app_notification, self, "Xfce4-terminal Themes Installed")

    def on_clicked_install_termite_themes(self,widget):
        command = 'pacman -S termite arcolinux-termite-themes-git --needed --noconfirm'
        Functions.subprocess.call(command.split(" "),
                        shell=False,
                        stdout=Functions.subprocess.PIPE,
                        stderr=Functions.subprocess.STDOUT)
        Functions.copy_func("/etc/skel/.config/termite", Functions.home + "/.config/", True)
        Functions.permissions(Functions.home + "/.config/termite")
        print("Installing termite arcolinux-termite-themes-git")
        GLib.idle_add(Functions.show_in_app_notification, self, "Termite Themes Installed")

    # def on_clicked_launch_alacritty_themes(self,widget):
    #     Functions.install_alacritty_themes(self)
    #     subprocess.call(["su - " + Functions.sudo_username + " -c " +  "/usr/bin/alacritty-themes"], shell=True)
    #     GLib.idle_add(Functions.show_in_app_notification, self, "Done")

    def on_clicked_reset_xfce4_terminal(self,widget):
        if os.path.isfile(Functions.xfce4_terminal_config + ".bak"):
            Functions.shutil.copy(Functions.xfce4_terminal_config + ".bak",
                                  Functions.xfce4_terminal_config)
            Functions.permissions(Functions.home + "/.config/xfce4/terminal")
            print("xfce4_terminal reset")

    def on_clicked_reset_alacritty(self,widget):
        if os.path.isfile(Functions.alacritty_config + ".bak"):
            Functions.shutil.copy(Functions.alacritty_config + ".bak",
                                  Functions.alacritty_config)
            Functions.permissions(Functions.home + "/.config/alacritty")
            print("Alacritty reset")

    def on_clicked_set_arcolinux_alacritty_theme(self,widget):
        if os.path.isfile(Functions.alacritty_config):
            Functions.shutil.copy(Functions.alacritty_arco,
                                  Functions.alacritty_config)
            Functions.permissions(Functions.home + "/.config/alacritty")
            print("Applied ArcoLinux Alacritty theme")

    #    #====================================================================
    #    #                       TERMITE
    #    #====================================================================

    def on_install_termite_themes(self, widget):
        self.btn_term.set_sensitive(False)
        ll = self.btn_term.get_child()
        ll.set_text("Installing ....")
        t1 = Functions.threading.Thread(target=self.install_term_themes, args=())
        t1.daemon = True
        t1.start()

    def install_term_themes(self):
        Functions.subprocess.run(['pkexec', 'pacman', '-S', 'arcolinux-termite-themes-git', '--noconfirm', '--needed'])
        Functions.copy_func("/etc/skel/.config/termite", Functions.home + "/.config/", True)
        Functions.permissions(Functions.home + "/.config/termite")
        GLib.idle_add(Functions.show_in_app_notification, self, "Themes Installed")

        GLib.idle_add(self.btn_term.set_sensitive, True)
        ll = self.btn_term.get_child()
        GLib.idle_add(ll.set_text, "Install Termite themes")
        GLib.idle_add(self.ls2.set_markup, "Please restart the <b>ArchLinux Tweak Tool</b>")

    def on_term_apply(self, widget):
        if self.term_themes.get_active_text() is not None:
            widget.set_sensitive(False)
            termite.set_config(self, self.term_themes.get_active_text())
            widget.set_sensitive(True)

    def on_term_reset(self, widget):
        if os.path.isfile(Functions.termite_config + ".bak"):
            Functions.shutil.copy(Functions.termite_config + ".bak",
                                  Functions.termite_config)
            Functions.show_in_app_notification(self,
                                               "Default Settings Applied")
            if Functions.os.path.isfile(Functions.config):
                Settings.write_settings("TERMITE", "theme", '')
                termite.get_themes(self.term_themes)

    #    #====================================================================
    #    #                       ZSH THEMES
    #    #====================================================================

    def on_zsh_apply_theme(self, widget):

        #create a .zshrc if it doesn't exist'
        if not os.path.isfile(Functions.zsh_config):
            Functions.shutil.copy(Functions.zshrc_arco,
                                  Functions.zsh_config)
            Functions.permissions(Functions.home + "/.zshrc")

        if self.zsh_themes.get_active_text() is not None:
            widget.set_sensitive(False)
            zsh_theme.set_config(self, self.zsh_themes.get_active_text())
            widget.set_sensitive(True)
            print("Applying zsh theme")

    def on_zsh_reset(self, widget):
        if os.path.isfile(Functions.zsh_config + ".bak"):
            Functions.shutil.copy(Functions.zsh_config + ".bak", Functions.zsh_config)
            Functions.permissions(Functions.home + "/.zshrc")
            Functions.permissions(Functions.home + "/.zshrc.bak")
            Functions.show_in_app_notification(self, "Default settings applied")
            print("Backup has been applied")
        else:
            Functions.shutil.copy("/usr/share/archlinux-tweak-tool/data/arco/.zshrc", Functions.home + "/.zshrc")
            Functions.permissions(Functions.home + "/.zshrc")
            Functions.show_in_app_notification(self, "Valid ~/.zshrc applied")
            print("Valid ~/.zshrc applied")


    def tozsh_apply(self,widget):
        # install missing applications
        Functions.install_zsh(self)
        # first make backup if there is a file
        if not Functions.os.path.isfile(Functions.zsh_config + ".bak") and Functions.os.path.isfile(Functions.zsh_config):
            Functions.shutil.copy(Functions.zsh_config,
                              Functions.zsh_config + ".bak")
            Functions.permissions(Functions.home + "/.zshrc")
            Functions.permissions(Functions.home + "/.zshrc.bak")
            print("We created a backup")
        if not Functions.os.path.isfile(Functions.zsh_config):
            try:
                Functions.shutil.copy("/usr/share/archlinux-tweak-tool/data/arco/.zshrc", Functions.home + "/.zshrc")
                Functions.permissions(Functions.home + "/.zshrc")
                print("Providing a valid zshrc")

            except Exception as e:
                print(e)

        command = 'sudo chsh ' + Functions.sudo_username + ' -s /bin/zsh'
        Functions.subprocess.call(command,
                        shell=True,
                        stdout=Functions.subprocess.PIPE,
                        stderr=Functions.subprocess.STDOUT)
        print("Shell changed to zsh for the user - logout")
        GLib.idle_add(Functions.show_in_app_notification, self, "Shell changed to zsh for user - logout")

    def tobash_apply(self,widget):
        command = 'sudo chsh ' + Functions.sudo_username + ' -s /bin/bash'
        Functions.subprocess.call(command,
                        shell=True,
                        stdout=Functions.subprocess.PIPE,
                        stderr=Functions.subprocess.STDOUT)
        print("Shell changed to bash for the user - logout")
        GLib.idle_add(Functions.show_in_app_notification, self, "Shell changed to bash for user - logout")

    def install_oh_my_zsh(self,widget):
        if os.path.exists("/usr/share/licenses/oh-my-zsh-git/LICENSE"):
            print("Oh-my-zsh-git already installed")
            pass
        else:
            install = 'pacman -S oh-my-zsh-git --noconfirm'
            try:
                subprocess.call(install.split(" "),
                                shell=False,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
                print("Installing oh-my-zsh-git")
            except Exception as e:
                print(e)
        GLib.idle_add(Functions.show_in_app_notification, self, "oh-my-zsh-git is installed")

    #The intent behind this function is to be a centralised image changer for all portions of ATT that need it
    #Currently utilising an if tree - this is not best practice: it should be a match: case tree.
    #But I have not yet got that working.
    def update_image(self, widget, image, theme_type, att_base, image_width, image_height):
        sample_path = ""
        preview_path = ""
        random_option = False
    # THIS CODE IS KEPT ON PURPOSE. DO NOT DELETE.
    # Once Python 3.10 is released and used widely, delete the if statements below the match blocks
    # and use the match instead. It is faster, and easier to maintain.
    #    match "zsh":
    #        case 'zsh':
    #            sample_path = att_base+"/images/zsh-sample.jpg"
    #            preview_path = att_base+"/images/zsh_previews/"+widget.get_active_text() + ".jpg"
    #        case 'qtile':
    #            sample_path = att_base+"/images/zsh-sample.jpg"
    #            previe_path = att_base+"/images/zsh_previews/"+widget.get_active_text() + ".jpg"
    #        case 'i3':
    #            sample_path = att_base+"/images/i3-sample.jpg"
    #            preview_path = att_base+"/themer_data/i3/"+widget.get_active_text() + ".jpg"
    #        case 'awesome':
    #            sample_path = att_base+"/images/i3-sample.jpg"
    #            preview_path = att_base+"/themer_data/awesomewm/"+widget.get_active_text() + ".jpg"
    #        case 'neofetch':
    #            sample_path = att_base + widget.get_active_text()
    #            preview_path = att_base + widget.get_active_text()
    #        case unknown_command:
    #            print("Function update_image passed an incorrect value for theme_type. Value passed was: " + theme_type)
    #            print("Remember that the order for using this function is: self, widget, image, theme_type, att_base_path, image_width, image_height.")
        if theme_type == "zsh":
            sample_path = att_base+"/images/zsh-sample.jpg"
            preview_path = att_base+"/images/zsh_previews/"+widget.get_active_text() + ".jpg"
            if widget.get_active_text() == "random":
                random_option = True
        elif theme_type == "qtile":
            sample_path = att_base+"/images/qtile-sample.jpg"
            preview_path = att_base+"/themer_data/qtile/"+widget.get_active_text() + ".jpg"
        elif theme_type == "i3":
            sample_path = att_base+"/images/i3-sample.jpg"
            preview_path = att_base+"/themer_data/i3/"+widget.get_active_text() + ".jpg"
        elif theme_type == "awesome":
        #Awesome section doesn't use a ComboBoxText, but a ComboBox - which has different properties.
            tree_iter = self.awesome_combo.get_active_iter()
            if tree_iter is not None:
                model = self.awesome_combo.get_model()
                row_id, name = model[tree_iter][:2]

            sample_path = att_base+"/images/i3-sample.jpg"
            preview_path = att_base+"/themer_data/awesomewm/"+name+".jpg"
        elif theme_type == "neofetch":
            sample_path = att_base + widget.get_active_text()
            preview_path = att_base + widget.get_active_text()
        else:
        #If we are doing our job correctly, this should never be shown to users. If it does, we have done something wrong as devs.
                print("Function update_image passed an incorrect value for theme_type. Value passed was: " + theme_type)
                print("Remember that the order for using this function is: self, widget, image, theme_type, att_base_path, image_width, image_height.")
        source_pixbuf = image.get_pixbuf()
        if os.path.isfile(preview_path) and not random_option:
            pixbuf = GdkPixbuf.Pixbuf().new_from_file_at_size(preview_path, image_width, image_height)
        else:
            pixbuf = GdkPixbuf.Pixbuf().new_from_file_at_size(sample_path, image_width, image_height)
        image.set_from_pixbuf(pixbuf)

    #    #====================================================================
    #    #                       FISH
    #    #====================================================================

    # if os.path.isfile("/usr/bin/fish"):
    #     self.fish.set_active(True)
    # else:
    #     fish.fish.set_active(False)

    def on_fish_toggle(self, widget, active):
        if widget.get_active():
            Functions.install_fish(self)
            self.fish.set_active(True)
            GLib.idle_add(Functions.show_in_app_notification, self, "Fish installed")
        else:
            Functions.remove_fish(self)
            self.fish.set_active(False)
            GLib.idle_add(Functions.show_in_app_notification, self, "Fish removed")

    def on_ohmyfish_toggle(self, widget, active):
        if widget.get_active():
            GLib.idle_add(Functions.show_in_app_notification, self, "Shell changed for user - logout")
        else:
            GLib.idle_add(Functions.show_in_app_notification, self, "Shell changed for user - login")

    def tofish_apply(self,widget):
        # install missing applications for ArcoLinuxD
        Functions.install_fish(self)
        # first make backup if there is a file
        if not Functions.os.path.isfile(Functions.home + "/.config/fish/config.fish" + ".bak") \
                    and Functions.os.path.isfile(Functions.home + "/.config/fish/config.fish"):
            Functions.shutil.copy(Functions.home + "/.config/fish/config.fish",
                              Functions.home + "/.config/fish/config.fish" + ".bak")
            Functions.permissions(Functions.home + "/.config/fish/config.fish.bak")
        if not Functions.os.path.isfile(Functions.home + "/.config/fish/config.fish"):
            Functions.shutil.copy("/etc/skel/.config/fish/config.fish",
                              Functions.home + "/.config/fish/config.fish")
            Functions.permissions(Functions.home + "/.config/fish/config.fish")

        command = 'sudo chsh ' + Functions.sudo_username + ' -s /usr/bin/fish'
        Functions.subprocess.call(command,
                        shell=True,
                        stdout=Functions.subprocess.PIPE,
                        stderr=Functions.subprocess.STDOUT)
        widget.set_sensitive(True)
        GLib.idle_add(Functions.show_in_app_notification, self, "Shell changed for user - logout")

    def on_fish_reset(self, widget):
        if os.path.isfile(Functions.home + "/.config/fish/config.fish.bak"):
            Functions.shutil.copy(Functions.home + "/.config/fish/config.fish.bak",
                                  Functions.home + "/.config/fish/config.fish")
        if not Functions.os.path.isfile(Functions.home + "/.config/fish/config.fish.bak"):
            Functions.shutil.copy("/etc/skel/.config/fish/config.fish",
                                  Functions.home + "/.config/fish/config.fish")

        Functions.permissions(Functions.home + "/.config/fish/config.fish")
        Functions.show_in_app_notification(self,
                                            "Default Settings Applied")

    #The intent behind this function is to be a centralised image changer for all portions of ATT that need it
    #Currently utilising an if tree - this is not best practice: it should be a match: case tree.
    #But I have not yet got that working.
    def update_image(self, widget, image, theme_type, att_base, image_width, image_height):
        sample_path = ""
        preview_path = ""
        random_option = False
    # THIS CODE IS KEPT ON PURPOSE. DO NOT DELETE.
    # Once Python 3.10 is released and used widely, delete the if statements below the match blocks
    # and use the match instead. It is faster, and easier to maintain.
    #    match "zsh":
    #        case 'zsh':
    #            sample_path = att_base+"/images/zsh-sample.jpg"
    #            preview_path = att_base+"/images/zsh_previews/"+widget.get_active_text() + ".jpg"
    #        case 'qtile':
    #            sample_path = att_base+"/images/zsh-sample.jpg"
    #            previe_path = att_base+"/images/zsh_previews/"+widget.get_active_text() + ".jpg"
    #        case 'i3':
    #            sample_path = att_base+"/images/i3-sample.jpg"
    #            preview_path = att_base+"/themer_data/i3/"+widget.get_active_text() + ".jpg"
    #        case 'awesome':
    #            sample_path = att_base+"/images/i3-sample.jpg"
    #            preview_path = att_base+"/themer_data/awesomewm/"+widget.get_active_text() + ".jpg"
    #        case 'neofetch':
    #            sample_path = att_base + widget.get_active_text()
    #            preview_path = att_base + widget.get_active_text()
    #        case unknown_command:
    #            print("Function update_image passed an incorrect value for theme_type. Value passed was: " + theme_type)
    #            print("Remember that the order for using this function is: self, widget, image, theme_type, att_base_path, image_width, image_height.")
        if theme_type == "zsh":
            sample_path = att_base+"/images/zsh-sample.jpg"
            preview_path = att_base+"/images/zsh_previews/"+widget.get_active_text() + ".jpg"
            if widget.get_active_text() == "random":
                random_option = True
        elif theme_type == "qtile":
            sample_path = att_base+"/images/qtile-sample.jpg"
            preview_path = att_base+"/themer_data/qtile/"+widget.get_active_text() + ".jpg"
        elif theme_type == "i3":
            sample_path = att_base+"/images/i3-sample.jpg"
            preview_path = att_base+"/themer_data/i3/"+widget.get_active_text() + ".jpg"
        elif theme_type == "awesome":
        #Awesome section doesn't use a ComboBoxText, but a ComboBox - which has different properties.
            tree_iter = self.awesome_combo.get_active_iter()
            if tree_iter is not None:
                model = self.awesome_combo.get_model()
                row_id, name = model[tree_iter][:2]

            sample_path = att_base+"/images/i3-sample.jpg"
            preview_path = att_base+"/themer_data/awesomewm/"+name+".jpg"
        elif theme_type == "neofetch":
            sample_path = att_base + widget.get_active_text()
            preview_path = att_base + widget.get_active_text()
        else:
        #If we are doing our job correctly, this should never be shown to users. If it does, we have done something wrong as devs.
                print("Function update_image passed an incorrect value for theme_type. Value passed was: " + theme_type)
                print("Remember that the order for using this function is: self, widget, image, theme_type, att_base_path, image_width, image_height.")
        source_pixbuf = image.get_pixbuf()
        if os.path.isfile(preview_path) and not random_option:
            pixbuf = GdkPixbuf.Pixbuf().new_from_file_at_size(preview_path, image_width, image_height)
        else:
            pixbuf = GdkPixbuf.Pixbuf().new_from_file_at_size(sample_path, image_width, image_height)
        image.set_from_pixbuf(pixbuf)

    #    #====================================================================
    #    #                       ARCOLINUX MIRRORLIST
    #    #===================================================================

    def on_click_launch_pace(self, widget):
        Functions.install_pace(self)
        subprocess.Popen("/usr/bin/pace",shell=False)

    #    #====================================================================
    #    #                       ARCOLINUX MIRRORLIST
    #    #===================================================================

    def on_click_reset_arcolinux_mirrorlist(self, widget):
        if not Functions.os.path.isfile(Functions.arcolinux_mirrorlist + ".bak"):
            Functions.shutil.copy(Functions.arcolinux_mirrorlist,
                                  Functions.arcolinux_mirrorlist + ".bak")

        if Functions.os.path.isfile(Functions.arcolinux_mirrorlist_original):
            Functions.shutil.copy(Functions.arcolinux_mirrorlist_original,
                                  Functions.arcolinux_mirrorlist)
            Functions.show_in_app_notification(self, "Original ArcoLinux mirrorlist is applied")
        Functions.restart_program()


#    #====================================================================
#    #                       NEOFETCH CONFIG
#    #====================================================================

    def on_apply_neo(self, widget):
        if not os.path.isfile(Functions.neofetch_config + ".bak"):
            Functions.shutil.copy(Functions.neofetch_config,
                                  Functions.neofetch_config + ".bak")
            Functions.permissions(Functions.neofetch_config + ".bak")
            Functions.shutil.copy(Functions.bash_config, Functions.bash_config + ".bak")
            Functions.shutil.copy(Functions.zsh_config, Functions.zsh_config + ".bak")

        small_ascii = "auto"

        if self.w3m.get_active():
            backend = "w3m"
            emblem = self.emblem.get_active_text()
        else:
            backend = "ascii"
            emblem = ""

            if not self.big_ascii.get_active() and not self.off.get_active():
                small_ascii = "arcolinux_small"
                backend = "ascii"
            elif not self.small_ascii.get_active() and not self.off.get_active():  # noqa
                backend = "ascii"

            else:
                backend = "off"

        neofetch.apply_config(self, backend, emblem, small_ascii)

    def on_reset_neo(self, widget):
        if os.path.isfile(Functions.neofetch_config + ".bak"):
            Functions.shutil.copy(Functions.neofetch_config + ".bak",
                                  Functions.neofetch_config)

            neofetch.pop_neofetch_box(self.emblem)
            backend = neofetch.check_backend()
            if backend == "ascii":
                self.asci.set_active(True)
                self.emblem.set_sensitive(False)
            else:
                self.w3m.set_active(True)

            neofetch.get_checkboxes(self)
            Functions.show_in_app_notification(self,
                                               "Default Settings Applied")

    def radio_toggled(self, widget):
        if self.w3m.get_active():
            self.emblem.set_sensitive(True)
            self.big_ascii.set_sensitive(False)
            self.small_ascii.set_sensitive(False)
            path = (Functions.home + "/.config/neofetch/" +
                    self.emblem.get_active_text())

            pixbuf6 = GdkPixbuf.Pixbuf().new_from_file_at_size(path, 145, 145)
            self.image4.set_from_pixbuf(pixbuf6)
            self.frame3.show()
            self.image4.show()

        elif self.asci.get_active():
            self.emblem.set_sensitive(False)
            self.big_ascii.set_sensitive(True)
            self.small_ascii.set_sensitive(True)
            self.image4.set_from_pixbuf(None)
            self.frame3.hide()
        else:
            self.big_ascii.set_sensitive(False)
            self.small_ascii.set_sensitive(False)
            self.image4.set_from_pixbuf(None)
            self.frame3.hide()
            self.emblem.set_sensitive(False)

    #When using this function to toggle a lolcat: utility = name of tool, e.g. neofetch
    def lolcat_toggle(self, widget, active, utility):
        #If set to active:
        util_str = utility
        if widget.get_active():
            utilities.install_util("lolcat")
            util_str = utility + " | lolcat" #The space here is CRITICAL
            #If the utility is currently not acive, activate it
            if utilities.get_util_state(self, utility) == False or utility == "neofetch":
                utilities.set_util_state(self, utility, True, True)
        #The below is to ensure that the check box on Neofetch always toggles to match correctly
        elif widget.get_active() == False and utility == "neofetch":
            utilities.set_util_state(self, utility, True, False)
        utilities.write_configs(utility, util_str)

    def util_toggle(self, widget, active, utility):
        util_str = utility
        if widget.get_active():
            util_str = utility
            utilities.install_util(utility)
            if utility == "neofetch":
                utilities.set_util_state(self, utility, True, utilities.get_lolcat_state(self, utility))
        else:
            util_str = "#" + utility
            #If the lolcat for the utility is on; best turn it off too.
            if utilities.get_lolcat_state(self, utility):
                utilities.set_util_state(self, utility, False, False)
            if utility == "neofetch":
                utilities.set_util_state(self, utility, False, False)
        utilities.write_configs(utility, util_str)

    # ====================================================================
    #                       Lightdm
    # ====================================================================

    def on_click_lightdm_apply(self, widget):
        if not Functions.os.path.isfile(Functions.lightdm_conf + ".bak"):
            Functions.shutil.copy(Functions.lightdm_conf,
                                  Functions.lightdm_conf + ".bak")

        if (self.sessions.get_active_text() is not None and self.autologin.get_active() is True) or self.autologin.get_active() is False:
            t1 = Functions.threading.Thread(target=lightdm.set_lightdm_value,
                                            args=(self,
                                                lightdm.get_lines(Functions.lightdm_conf),  # noqa
                                                Functions.sudo_username,
                                                self.sessions.get_active_text(),
                                                self.autologin.get_active()))
            t1.daemon = True
            t1.start()
            print("Settings saved successfully")
        else:
            Functions.show_in_app_notification(self, "Need to select desktop first")

    def on_click_lightdm_reset(self, widget):
        if Functions.os.path.isfile(Functions.lightdm_conf + ".bak"):
            Functions.shutil.copy(Functions.lightdm_conf + ".bak",
                                  Functions.lightdm_conf)

        if "#" in lightdm.check_lightdm(lightdm.get_lines(Functions.lightdm_conf), "autologin-user="):  # noqa
            self.autologin.set_active(False)
        else:
            self.autologin.set_active(True)

        print("Default Settings Applied")
        Functions.show_in_app_notification(self, "Default Settings Applied")

    def on_autologin_activated(self, widget, gparam):
        if widget.get_active():
            command = 'groupadd autologin'
            try:
                Functions.subprocess.call(command.split(" "),
                            shell=False,
                            stdout=Functions.subprocess.PIPE,
                            stderr=Functions.subprocess.STDOUT)
            except Exception as e:
                    print(e)

            #print("We added the group autologin or checked that it exists")
            self.sessions.set_sensitive(True)
        else:
            self.sessions.set_sensitive(False)

    def on_click_att_lightdm_clicked(self, desktop):
        command = 'pacman -S lightdm lightdm-gtk-greeter lightdm-gtk-greeter-settings --noconfirm'
        Functions.subprocess.call(command.split(" "),
                        shell=False,
                        stdout=Functions.subprocess.PIPE,
                        stderr=Functions.subprocess.STDOUT)
        print("We installed lightdm lightdm-gtk-greeter lightdm-gtk-greeter-settings")

        command = 'systemctl enable lightdm.service -f'
        Functions.subprocess.call(command.split(" "),
                        shell=False,
                        stdout=Functions.subprocess.PIPE,
                        stderr=Functions.subprocess.STDOUT)
        print("We enabled lightdm")

        GLib.idle_add(Functions.show_in_app_notification, self, "Lightdm has been installed and enabled - reboot")
        Functions.restart_program()

    def on_click_lightdm_enable(self, desktop):
        command = 'systemctl enable lightdm.service -f'
        Functions.subprocess.call(command.split(" "),
                        shell=False,
                        stdout=Functions.subprocess.PIPE,
                        stderr=Functions.subprocess.STDOUT)
        print("Lightdm has been enabled - reboot")
        GLib.idle_add(Functions.show_in_app_notification, self, "Lightdm has been enabled - reboot")

    def on_click_lightdm_slick(self, desktop):
        #self.on_click_att_lightdm_clicked(desktop)
        #self.on_click_lightdm_enable(desktop)
        command = '/usr/share/archlinux-tweak-tool/data/any/archlinux-install-activate-lightdm-slickgreeter'
        Functions.subprocess.call(command.split(" "),
                        shell=False,
                        stdout=Functions.subprocess.PIPE,
                        stderr=Functions.subprocess.STDOUT)
        print("Lightdm slickgreeter has been installed and enabled - reboot")
        GLib.idle_add(Functions.show_in_app_notification, self, "Lightdm-slickgreeter installed - Reboot now")

    # ====================================================================
    #                       SDDM
    # ====================================================================

    def on_click_sddm_apply(self, widget):
        #if not Functions.os.path.isfile(Functions.sddm_conf + ".bak"):
        #    Functions.shutil.copy(Functions.sddm_conf,
        #                          Functions.sddm_conf + ".bak")
        command = 'systemctl enable sddm.service -f'
        Functions.subprocess.call(command.split(" "),
                        shell=False,
                        stdout=Functions.subprocess.PIPE,
                        stderr=Functions.subprocess.STDOUT)
        print("We enabled sddm.service")

        if not os.path.isdir(Functions.sddm_default_d2_dir):
            try:
                os.mkdir(Functions.sddm_default_d2_dir)
            except Exception as e:
                print(e)

        if (self.sessions_sddm.get_active_text() is not None and self.theme_sddm.get_active_text() is not None and self.autologin_sddm.get_active() is True) or (self.autologin_sddm.get_active() is False and self.theme_sddm.get_active_text() is not None) :
            t1 = Functions.threading.Thread(target=sddm.set_sddm_value,
                                            args=(self,
                                                sddm.get_sddm_lines(Functions.sddm_default_d2),  # noqa
                                                Functions.sudo_username,
                                                self.sessions_sddm.get_active_text(),
                                                self.autologin_sddm.get_active(),
                                                self.theme_sddm.get_active_text()))
            t1.daemon = True
            t1.start()

            t1 = Functions.threading.Thread(target=sddm.set_sddm_cursor,
                                            args=(self,
                                            sddm.get_sddm_lines(Functions.sddm_default),  # noqa
                                            self.entry_cursor_name.get_text()))
            t1.daemon = True
            t1.start()
            print("Settings Saved Successfully")
            GLib.idle_add(Functions.show_in_app_notification, self, "Settings Saved Successfully")

        else:
            print("You need to select desktop and/or theme first")
            Functions.show_in_app_notification(self, "You need to select desktop and/or theme first")

    def on_click_sddm_reset(self, widget):
        if Functions.os.path.isfile(Functions.sddm_default_d2):
            if "#" in sddm.check_sddm(sddm.get_sddm_lines(Functions.sddm_default_d2), "User="):  # noqa
                self.autologin_sddm.set_active(False)
            else:
                self.autologin_sddm.set_active(True)
            print("Your sddm.conf backup is now applied")
            Functions.show_in_app_notification(self, "Your sddm.conf backup is now applied")
        else:
            print("We did not find a backup file for sddm.conf")
            Functions.show_in_app_notification(self, "We did not find a backup file for sddm.conf")

    def on_click_sddm_reset_original(self, widget):
        if not os.path.isdir(Functions.sddm_default_d2_dir):
            try:
                os.mkdir(Functions.sddm_default_d2_dir)
            except Exception as e:
                print(e)
        if Functions.sddm_conf == "/etc/sddm.conf.d/kde_settings.conf":
            Functions.shutil.copy(Functions.sddm_default_d_sddm_original_1,
                                  Functions.sddm_default_d1)
            Functions.shutil.copy(Functions.sddm_default_d_sddm_original_2,
                                  Functions.sddm_default_d2)
        else:
            Functions.shutil.copy(Functions.sddm_default_original,
                                  Functions.sddm_default)

        if "#" in sddm.check_sddm(sddm.get_sddm_lines(Functions.sddm_default_d2), "User="):  # noqa
            self.autologin_sddm.set_active(False)
        else:
            self.autologin_sddm.set_active(True)

        print("The ArcoLinux sddm configuration is now applied")
        print("Both files have been changed /etc/sddm.conf and /etc/sddm.conf.d/kde_settings.conf")
        Functions.show_in_app_notification(self, "The ArcoLinux sddm.conf is now applied")

    def on_click_no_sddm_reset_original(self, widget):
        if not os.path.isdir(Functions.sddm_default_d2_dir):
            try:
                os.mkdir(Functions.sddm_default_d2_dir)
            except Exception as e:
                print(e)
        if Functions.os.path.isfile(Functions.sddm_default_d_sddm_original_1):
            Functions.shutil.copyfile(Functions.sddm_default_d_sddm_original_1,
                                  Functions.sddm_default_d1)
            Functions.shutil.copyfile(Functions.sddm_default_d_sddm_original_2,
                                  Functions.sddm_default_d2)
        print("The ArcoLinux sddm configuration is now applied")
        Functions.show_in_app_notification(self, "The ArcoLinux sddm configuration is now applied")

    def on_autologin_sddm_activated(self, widget, gparam):
        if widget.get_active():
            command = 'groupadd autologin'
            try:
                Functions.subprocess.call(command.split(" "),
                            shell=False,
                            stdout=Functions.subprocess.PIPE,
                            stderr=Functions.subprocess.STDOUT)
            except Exception as e:
                    print(e)

            #print("We added the group autologin or checked that it exists")
            self.sessions_sddm.set_sensitive(True)
        else:
            self.sessions_sddm.set_sensitive(False)

    def on_click_install_sddm_themes(self,widget):
        command = 'pacman -S arcolinux-meta-sddm-themes --needed --noconfirm'
        Functions.subprocess.call(command.split(" "),
                        shell=False,
                        stdout=Functions.subprocess.PIPE,
                        stderr=Functions.subprocess.STDOUT)
        print("We installed all ArcoLinux sddm themes")
        GLib.idle_add(Functions.show_in_app_notification, self, "ArcoLinux Sddm Themes Installed")
        Functions.restart_program()

    def on_click_remove_sddm_themes(self,widget):
        command = 'pacman -Rss arcolinux-meta-sddm-themes --noconfirm'
        Functions.subprocess.call(command.split(" "),
                        shell=False,
                        stdout=Functions.subprocess.PIPE,
                        stderr=Functions.subprocess.STDOUT)
        print("We removed all ArcoLinux sddm themes")
        GLib.idle_add(Functions.show_in_app_notification, self, "ArcoLinux Sddm themes were removed")

        if self.keep_default_theme.get_active() is True:
            command = 'pacman -S arcolinux-sddm-simplicity-git --needed --noconfirm'
            Functions.subprocess.call(command.split(" "),
                            shell=False,
                            stdout=Functions.subprocess.PIPE,
                            stderr=Functions.subprocess.STDOUT)
            print("We installed the default ArcoLinux sddm theme again")
            GLib.idle_add(Functions.show_in_app_notification, self, "ArcoLinux Sddm themes were removed except default")

    #if no sddm - press 1
    def on_click_att_sddm_clicked(self, desktop):
        command = 'pacman -S sddm --noconfirm --needed'
        Functions.subprocess.call(command.split(" "),
                        shell=False,
                        stdout=Functions.subprocess.PIPE,
                        stderr=Functions.subprocess.STDOUT)
        print("We installed sddm")

        command = 'pacman -S arcolinux-sddm-simplicity-git --noconfirm --needed'
        Functions.subprocess.call(command.split(" "),
                        shell=False,
                        stdout=Functions.subprocess.PIPE,
                        stderr=Functions.subprocess.STDOUT)
        print("We installed arcolinux-sddm-simplicity-git")

        command = 'pacman -S bibata-cursor-theme-bin --noconfirm --needed'
        Functions.subprocess.call(command.split(" "),
                        shell=False,
                        stdout=Functions.subprocess.PIPE,
                        stderr=Functions.subprocess.STDOUT)
        print("We installed bibata-cursor-theme-bin")

        command = 'systemctl enable sddm.service -f'
        Functions.subprocess.call(command.split(" "),
                        shell=False,
                        stdout=Functions.subprocess.PIPE,
                        stderr=Functions.subprocess.STDOUT)
        print("We enabled sddm.service")
        GLib.idle_add(Functions.show_in_app_notification, self, "Sddm has been installed and enabled - reboot")

        if not os.path.isdir(Functions.sddm_default_d2_dir):
            try:
                os.mkdir(Functions.sddm_default_d2_dir)
            except Exception as e:
                print(e)

        if Functions.os.path.isfile(Functions.sddm_default_d_sddm_original_1):
            Functions.shutil.copyfile(Functions.sddm_default_d_sddm_original_1,
                                  Functions.sddm_default_d1)
            Functions.shutil.copyfile(Functions.sddm_default_d_sddm_original_2,
                                  Functions.sddm_default_d2)
        print("The ArcoLinux sddm configuration is now applied")
        Functions.show_in_app_notification(self, "The ArcoLinux sddm configuration is now applied")
        Functions.restart_program()

    def on_click_sddm_enable(self, desktop):
        command = 'systemctl enable sddm.service -f'
        Functions.subprocess.call(command.split(" "),
                        shell=False,
                        stdout=Functions.subprocess.PIPE,
                        stderr=Functions.subprocess.STDOUT)
        print("We enabled sddm.service")
        GLib.idle_add(Functions.show_in_app_notification, self, "Sddm has been enabled - reboot")

    def on_launch_adt_clicked(self, desktop):
        Functions.install_adt(self)
        subprocess.Popen("/usr/local/bin/arcolinux-desktop-trasher")
        GLib.idle_add(Functions.show_in_app_notification, self, "ArcoLinux Desktop Trasher launched")
        print("We started ADT")

    def on_refresh_att_clicked(self, desktop):
        Functions.restart_program()

    # ====================================================================
    #                       USER
    # ====================================================================

    def on_click_user_apply(self, widget):
        user.create_user(self)

    # ====================================================================
    #                       FIXES
    # ====================================================================

    def on_click_fix_pacman_keys(self,widget):
        Functions.install_alacritty(self)
        Functions.subprocess.call("alacritty --hold -e /usr/share/archlinux-tweak-tool/data/any/fix-pacman-databases-and-keys",
                        shell=True,
                        stdout=Functions.subprocess.PIPE,
                        stderr=Functions.subprocess.STDOUT)
        GLib.idle_add(Functions.show_in_app_notification, self, "Pacman keys fixed")

    def on_click_fix_mainstream(self,widget):
        command = 'alacritty --hold -e /usr/share/archlinux-tweak-tool/data/any/set-mainstream-servers'
        Functions.subprocess.call(command.split(" "),
                        shell=False,
                        stdout=Functions.subprocess.PIPE,
                        stderr=Functions.subprocess.STDOUT)

        GLib.idle_add(Functions.show_in_app_notification, self, "Mainstream servers have been saved")

    def on_click_get_arch_mirrors(self,widget):
        Functions.install_reflector(self)
        Functions.subprocess.call("alacritty --hold -e /usr/share/archlinux-tweak-tool/data/any/archlinux-get-mirrors-reflector",
                        shell=True,
                        stdout=Functions.subprocess.PIPE,
                        stderr=Functions.subprocess.STDOUT)
        GLib.idle_add(Functions.show_in_app_notification, self, "Fastest Arch Linux servers saved")

    def on_click_get_arch_mirrors2(self,widget):
        Functions.subprocess.call("alacritty --hold -e /usr/share/archlinux-tweak-tool/data/any/archlinux-get-mirrors-rate-mirrors",
                        shell=True,
                        stdout=Functions.subprocess.PIPE,
                        stderr=Functions.subprocess.STDOUT)
        GLib.idle_add(Functions.show_in_app_notification, self, "Fastest Arch Linux servers saved")


    def on_click_fix_sddm_conf(self,widget):
        command = 'alacritty --hold -e /usr/share/archlinux-tweak-tool/data/arco/bin/arcolinux-fix-sddm-config'
        Functions.subprocess.call(command,
                        shell=True,
                        stdout=Functions.subprocess.PIPE,
                        stderr=Functions.subprocess.STDOUT)
        GLib.idle_add(Functions.show_in_app_notification, self, "Saved the original /etc/sddm.conf")

    def on_click_fix_pacman_conf(self,widget):
        command = 'alacritty --hold -e /usr/local/bin/arcolinux-fix-pacman-conf'
        Functions.subprocess.call(command,
                        shell=True,
                        stdout=Functions.subprocess.PIPE,
                        stderr=Functions.subprocess.STDOUT)
        GLib.idle_add(Functions.show_in_app_notification, self, "Saved the original /etc/pacman.conf")

    def on_click_fix_pacman_gpg_conf(self,widget):
        if not os.path.isfile(Functions.gpg_conf + ".bak"):
            Functions.shutil.copy(Functions.gpg_conf,
                            Functions.gpg_conf + ".bak")
        Functions.shutil.copy(Functions.gpg_conf_original,
                            Functions.gpg_conf)

        GLib.idle_add(Functions.show_in_app_notification, self, "The new /etc/pacman.d/gnupg/gpg.conf has been saved")

    def on_click_fix_pacman_gpg_conf_local(self,widget):
        if not os.path.isdir(Functions.home + "/.gnupg"):
            try:
                Functions.os.makedirs(Functions.home + "/.gnupg", 0o766)
                Functions.permissions(Functions.home + "/.gnupg")
            except Exception as e:
                print(e)

        if not os.path.isfile(Functions.gpg_conf_local + ".bak"):
            try:
                Functions.shutil.copy(Functions.gpg_conf_local,
                                Functions.gpg_conf_local + ".bak")
                Functions.permissions(Functions.gpg_conf_local + ".bak")
            except Exception as e:
                print(e)

        Functions.shutil.copy(Functions.gpg_conf_local_original,
                            Functions.gpg_conf_local)
        Functions.permissions(Functions.gpg_conf_local)

        GLib.idle_add(Functions.show_in_app_notification, self, "The new ~/.gnupg/gpg.conf has been saved")

#    #====================================================================
#    #                       DESKTOPR
#    #====================================================================

    def on_d_combo_changed(self, widget):
        try:
            pixbuf3 = GdkPixbuf.Pixbuf().new_from_file_at_size(base_dir +
                                                            "/desktop_data/" +
                                                            self.d_combo.get_active_text() + ".jpg",  # noqa
                                                            345,
                                                            345)
            self.image_DE.set_from_pixbuf(pixbuf3)
        except:  # noqa
            self.image_DE.set_from_pixbuf(None)
        if desktopr.check_desktop(self.d_combo.get_active_text()):
            self.desktop_status.set_text("This desktop is installed")
        else:
            self.desktop_status.set_text("This desktop is NOT installed")

    def on_uninstall_clicked(self, widget):
        secs = Settings.read_section()
        if "DESKTOP" in secs:
            desktopr.uninstall_desktop_check(self,
                                             self.d_combo.get_active_text())
        else:
            Functions.show_in_app_notification(self,
                                               "You Must Set Default First")

    def on_install_clicked(self, widget, state):
        Functions.create_log(self)
        # if desktopr.check_desktop(self.d_combo.get_active_text()) is not True:
        print("installing {}".format(self.d_combo.get_active_text()))
        desktopr.check_lock(self,self.d_combo.get_active_text(),state)

        # desktopr.install_desktop(self, self.d_combo.get_active_text())

    #TO ASK
    # def on_arco_repo_clicked(self, active):

    #     self.on_pacman_arepo_toggle(self)
    #     self.on_pacman_a3p_toggle(self)
    #     self.on_pacman_axl_toggle(self)

    def on_default_clicked(self, widget):
        Functions.create_log(self)
        if desktopr.check_desktop(self.d_combo.get_active_text()) is True:
            secs = Settings.read_section()
            if "DESKTOP" in secs:
                Settings.write_settings("DESKTOP",
                                        "default",
                                        self.d_combo.get_active_text())
            else:
                Settings.new_settings("DESKTOP",
                                      {"default": self.d_combo.get_active_text()})
        else:
            Functions.show_in_app_notification(self,
                                               "That desktop is not installed")

#    #====================================================================
#    #                       autostart
#    #====================================================================
    def on_comment_changed(self, widget):
        if len(self.txtbox1.get_text()) >= 3 and len(self.txtbox2.get_text()) >= 3:
            self.abutton.set_sensitive(True)

    #autostart toggle on and off
    def on_auto_toggle(self, widget, data, lbl):
        failed = False
        try:
            with open(Functions.autostart + lbl + ".desktop", "r") as f:
                lines = f.readlines()
                f.close()
            try:
                pos = Functions._get_position(lines, "Hidden=")
            except:
                failed = True
                with open(Functions.autostart + lbl + ".desktop", "a") as f:
                    f.write("Hidden=" + str(not widget.get_active()).lower())
                    f.close()
        except:
            pass
        if not failed:
            val = lines[pos].split("=")[1].strip()
            lines[pos] = lines[pos].replace(val, str(not widget.get_active()).lower())
            with open(Functions.autostart + lbl + ".desktop", "w") as f:
                f.writelines(lines)
                f.close()

    # remove file from ~/.config/autostart
    def on_auto_remove_clicked(self, widget, data, listbox, lbl):
        os.unlink(Functions.autostart + lbl + ".desktop")
        print("Removed item from ~/.config/autostart/")
        self.vvbox.remove(listbox)

    def clear_autostart(self):
        for x in self.vvbox.get_children():
            self.vvbox.remove(x)

    def load_autostart(self, files):
        self.clear_autostart()

        for x in files:
            self.add_row(x)

    def add_row(self, x):
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        vbox2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        lbl = Gtk.Label(xalign=0)
        lbl.set_text(x)

        swtch = Gtk.Switch()
        swtch.connect("notify::active", self.on_auto_toggle, lbl.get_text())
        swtch.set_active(autostart.get_startups(self, lbl.get_text()))

        listbox = Gtk.ListBox()

        fbE = Gtk.EventBox()

        pbfb = GdkPixbuf.Pixbuf().new_from_file_at_size(
            os.path.join(base_dir, 'images/remove.png'), 28, 28)
        fbimage = Gtk.Image().new_from_pixbuf(pbfb)

        fbE.add(fbimage)

        fbE.connect("button_press_event",
                    self.on_auto_remove_clicked,
                    listbox,
                    lbl.get_text())

        fbE.set_property("has-tooltip", True)

        fbE.connect("query-tooltip", self.tooltip_callback, "Remove")

        hbox.pack_start(lbl, False, False, 0)
        hbox.pack_end(fbE, False, False, 0)
        vbox2.pack_start(swtch, False, False, 10)
        hbox.pack_end(vbox2, False, False, 0)

        vbox1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        vbox1.pack_start(hbox, False, False, 5)

        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        listboxrow = Gtk.ListBoxRow()
        listboxrow.add(vbox1)
        listbox.add(listboxrow)

        self.vvbox.pack_start(listbox, False, False, 0)
        self.vvbox.show_all()

    def on_remove_auto(self, widget):
        selection = self.treeView4.get_selection()
        model, paths = selection.get_selected_rows()

        # Get the TreeIter instance for each path
        for path in paths:
            iter = model.get_iter(path)
            # Remove the ListStore row referenced by iter
            value = model.get_value(iter, 1)
            model.remove(iter)
            Functions.os.unlink(Functions.home + "/.config/autostart/" + value + ".desktop")  #  noqa

    def on_add_autostart(self, widget):
        if len(self.txtbox1.get_text()) > 1 and len(self.txtbox2.get_text()) > 1:  # noqa
            autostart.add_autostart(self, self.txtbox1.get_text(),
                                    self.txtbox2.get_text(),
                                    self.txtbox3.get_text())

    def on_exec_browse(self, widget):

        dialog = Gtk.FileChooserDialog(
            title="Please choose a file",
            action=Gtk.FileChooserAction.OPEN)

        dialog.set_select_multiple(False)
        dialog.set_show_hidden(False)
        dialog.set_current_folder(Functions.home)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Open",
                           Gtk.ResponseType.OK)
        dialog.connect("response", self.open_response_auto)

        dialog.show()

    def open_response_auto(self, dialog, response):
        if response == Gtk.ResponseType.OK:
            print(dialog.get_filenames())
            foldername = dialog.get_filenames()
            # for item in foldername:
            self.txtbox2.set_text(foldername[0])
            dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()

#    #====================================================================
#    #                       polybar
#    #====================================================================

    def on_polybar_apply_clicked(self, widget):
        if self.pbrbutton.get_active():
            state = True
        else:
            state = False

        polybar.set_config(self, self.pbcombo.get_active_text(), state)
        if Functions.os.path.isfile(polybar.launch):
            Functions.show_in_app_notification(self, "Restart polybar to see changes")
        else:
            Functions.MessageBox(self, "ERROR!!", "You dont seem to have a <b>launch.sh</b> file to launch/relaunch polybar")

    def on_pb_browse_config(self, widget):
        dialog = Gtk.FileChooserDialog(title="Please choose a file", action=Gtk.FileChooserAction.OPEN)
        dialog.set_select_multiple(False)

        dialog.set_current_folder(Functions.home)
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Open", Gtk.ResponseType.OK)
        dialog.connect("response", self.open_config_response)

        dialog.show()

    def on_pb_browse_image(self, widget):
        dialog = Gtk.FileChooserDialog(title="Please choose a file", action=Gtk.FileChooserAction.OPEN)
        dialog.set_select_multiple(False)
        filter = Gtk.FileFilter()
        filter.set_name("IMAGE Files")
        filter.add_mime_type("image/png")
        filter.add_mime_type("image/jpg")
        filter.add_mime_type("image/jpeg")
        dialog.set_filter(filter)
        dialog.set_current_folder(Functions.home)
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Open", Gtk.ResponseType.OK)
        dialog.connect("response", self.open_image_response)

        dialog.show()

    def open_image_response(self, dialog, response):

        if response == Gtk.ResponseType.OK:
            self.pbtextbox2.set_text(dialog.get_filename())
            dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()

    def open_config_response(self, dialog, response):

        if response == Gtk.ResponseType.OK:
            self.pbtextbox1.set_text(dialog.get_filename())
            dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()

    def on_pb_import_clicked(self, widget):
        polybar.import_config(self, self.pbtextbox1.get_text(), self.pbtextbox2.get_text())

    def on_pb_change_item(self, widget):
        try:
            pixbuf = GdkPixbuf.Pixbuf().new_from_file_at_size(Functions.config_dir + '/images/' + widget.get_active_text() + '.jpg', 385, 385)
            self.pbimage.set_from_pixbuf(pixbuf)
        except:
            self.pbimage.set_from_pixbuf(None)

#    #====================================================================
#    #                       SkelApp
#    #====================================================================

    def on_bashrc_upgrade(self, widget):
        skelapp.button_toggles(self, False)
        t1 = Functions.threading.Thread(target=skelapp.bash_upgrade,
                                        args=(self,))
        t1.daemon = True
        t1.start()
    # ======REMOVE ITEMS TO TREEVIEW=============

    def on_remove_fixed(self, widget):
        selection = self.treeView.get_selection()
        model, paths = selection.get_selected_rows()

        # Get the TreeIter instance for each path
        for path in paths:
            iter = model.get_iter(path)
            # Remove the ListStore row referenced by iter
            model.remove(iter)

#    # ======ADD ITEMS TO TREEVIEW================

    def on_browse_fixed(self, widget):
        if self.rbutton3.get_active():
            dialog = Gtk.FileChooserDialog(
                title="Please choose a file",
                action=Gtk.FileChooserAction.OPEN)
        elif self.rbutton4.get_active():
            dialog = Gtk.FileChooserDialog(
                title="Please choose a folder",
                action=Gtk.FileChooserAction.SELECT_FOLDER)

        dialog.set_select_multiple(True)
        dialog.set_show_hidden(True)
        dialog.set_current_folder("/etc/skel")
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Open",
                           Gtk.ResponseType.OK)
        dialog.connect("response", self.open_response_skel)

        dialog.show()

    def open_response_skel(self, dialog, response):
        if response == Gtk.ResponseType.OK:
            print(dialog.get_filenames())
            foldername = dialog.get_filenames()
            # for item in foldername:
            self.stores.append(foldername)
            dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
#    # ===============RUN SKEL================

    def on_button_fetch_clicked(self, widget):
        skelapp.button_toggles(self, False)
        skelapp.skel_check(self)

    def on_backup_clicked(self, widget):
        skelapp.button_toggles(self, False)
        skelapp.setMessage(self.label_info, "Running Backup")
        t1 = Functions.threading.Thread(target=skelapp.processing,
                                        args=(self,
                                              "BACKUP",
                                              self.label_info,
                                              self.progressbar,))
        t1.daemon = True
        t1.start()

    def backs_changed(self, widget):
        skelapp.refresh_inner(self)

    def on_refresh_clicked(self, widget):
        skelapp.refresh(self)

    def on_restore_inner_clicked(self, widget):
        skelapp.button_toggles(self, False)
        skelapp.setMessage(self.label_info, "Running Restore ....")

        t1 = Functions.threading.Thread(target=skelapp.restore_item,
                                        args=(self,))
        t1.daemon = True
        t1.start()

#    # ===========================================
#    #			DELETE BACKUP Section
#    # ===========================================

    def on_delete_inner_clicked(self, widget):
        skelapp.button_toggles(self, False)
        t1 = Functions.threading.Thread(
            target=skelapp.Delete_Inner_Backup, args=(self,))
        t1.daemon = True
        t1.start()

    def on_delete_clicked(self, widget):
        skelapp.button_toggles(self, False)
        t1 = Functions.threading.Thread(target=skelapp.Delete_Backup,
                                        args=(self,))
        t1.daemon = True
        t1.start()

#    # ===========================================
#    #		DELETE ALL BACKUP Section
#    # ===========================================

    def on_flush_clicked(self, widget):
        skelapp.button_toggles(self, False)
        md = Gtk.MessageDialog(parent=self, flags=0,
                               message_type=Gtk.MessageType.INFO,
                               buttons=Gtk.ButtonsType.YES_NO,
                               text="Are you Sure?")
        md.format_secondary_markup(
            "Are you sure you want to delete all your backups?")

        result = md.run()

        md.destroy()

        if result in (Gtk.ResponseType.OK, Gtk.ResponseType.YES):
            # self.button_toggles(False)
            t1 = Functions.threading.Thread(target=skelapp.Flush_All,
                                            args=(self,))
            t1.daemon = True
            t1.start()
        else:
            skelapp.button_toggles(self, True)

# ====================================================================
#                       MAIN
# ====================================================================


def signal_handler(sig, frame):
    print('\nATT is Closing.')
    os.unlink("/tmp/att.lock")
    Gtk.main_quit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    #These lines offer protection and grace when a kernel has obfuscated or removed basic OS functionality.
    os_function_support = True
    try:
        os.getlogin()
    except:
        os_function_support = False
    if not os.path.isfile("/tmp/att.lock") and os_function_support:
        with open("/tmp/att.pid", "w") as f:
            f.write(str(os.getpid()))
            f.close()
        style_provider = Gtk.CssProvider()
        style_provider.load_from_path(base_dir + "/att.css")

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        w = Main()
        w.show_all()
        Gtk.main()
    else:
        md = ""

        if os_function_support:
            md = Gtk.MessageDialog(parent=Main(),
                                   flags=0,
                                   message_type=Gtk.MessageType.INFO,
                                   buttons=Gtk.ButtonsType.YES_NO,
                                   text="Lock File Found")
            md.format_secondary_markup(
                "The lock file has been found. This indicates there is already an instance of <b>ArchLinux Tweak Tool</b> running.\n\
    click yes to remove the lock file and try running again")  # noqa
        else:
            md = Gtk.MessageDialog(parent=Main(),
                                   flags=0,
                                   message_type=Gtk.MessageType.INFO,
                                   buttons=Gtk.ButtonsType.CLOSE,
                                   text="Kernel Not Supported")
            md.format_secondary_markup(
                "Your current kernel does not support basic os function calls. <b>ArchLinux Tweak Tool</b> requires these to work.")  # noqa

        result = md.run()
        md.destroy()

        if result in (Gtk.ResponseType.OK, Gtk.ResponseType.YES):
            pid = ""
            with open("/tmp/att.pid", "r") as f:
                line = f.read()
                pid = line.rstrip().lstrip()
                f.close()

            if Functions.checkIfProcessRunning(int(pid)):
                Functions.MessageBox("Application Running!",
                                     "You first need to close the existing application")  # noqa
            else:
                os.unlink("/tmp/att.lock")
