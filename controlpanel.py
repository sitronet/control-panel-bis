#!/usr/bin/python3

__author__ = "Noël"
__copyright__ = "2025 may"
__credits__ = ["Noël", "c'est moi"]
__license__ = "GPL 2.0 , 3.0"
__version__ = "0.0.a"
__maintainer__ = "??"
__email__ = "rondrach  (at)  gmail"
__status__ = "Alpha release"

import re
import socket

import kivy
kivy.require('2.1.0')

from kivy.config import Config

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty
from kivy.uix.spinner import Spinner

import subprocess

from kivy.core.window import Window, Keyboard

Config.set('graphics', 'resizable', True)

class SqueezeliteStatWindow(Screen):

    def enable(self):
        try:
            resultat = subprocess.run(['sudo', 'systemctl', '--no-pager', 'enable', 'squeezelite'],
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise
        if resultat.returncode == 0:
            self.ids.resultatcommande.text = 'Enable: Success'
        else:
            self.ids.resultatcommande.text = 'Enable: Fail'
        if resultat.stdout:
            self.ids.resultatcommande.text = str(resultat.stdout)
        if resultat.stderr:
            self.ids.resultatcommande.text = str(resultat.stderr)

    def disable(self):
        try:
            resultat = subprocess.run(['sudo', 'systemctl', '--no-pager', 'disable', 'squeezelite'],
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise
        if resultat.returncode == 0:
            self.ids.resultatcommande.text = 'Disable: Success'
        else:
            self.ids.resultatcommande.text = 'Disable: Fail'
        if resultat.stdout:
            self.ids.resultatcommande.text = str(resultat.stdout)
        if resultat.stderr:
            self.ids.resultatcommande.text = str(resultat.stderr)

    def start(self):

        try:
            resultat = subprocess.run(['sudo', 'systemctl', '--no-pager', 'start', 'squeezelite'],
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise
        if resultat.returncode == 0:
            self.ids.resultatcommande.text = 'Start: Success'
        else:
            self.ids.resultatcommande.text = 'Start: Fail'
        if resultat.stdout:
            lines = resultat.stdout.splitlines()
            self.ids.resultatcommande.text = str(resultat.stdout)
            #print('Sortie : ' + resultat.stdout)
        if resultat.stderr:
            lines = resultat.stderr.splitlines()
            self.ids.resultatcommande.text = str(resultat.stderr)
            #print('erreur : ' + resultat.stderr)
        #sm.current = "accueil"

    def stop(self):
        try:
            resultat = subprocess.run(['sudo', 'systemctl', '--no-pager', 'stop', 'squeezelite'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise
        if resultat.returncode == 0:
            self.ids.resultatcommande.text = 'Stop Success'
        else:
            self.ids.resultatcommande.text = 'Stop Fail'
        if resultat.stdout:
            lines = resultat.stdout.splitlines()
            self.ids.resultatcommande.text = str(resultat.stdout)
            print('Sortie : ' + resultat.stdout)
        if resultat.stderr:
            lines = resultat.stderr.splitlines()
            self.ids.resultatcommande.text = str(resultat.stderr)
            print('erreur : ' + resultat.stderr)

    def status(self):
        try:
            resultat = subprocess.run(['sudo', 'systemctl', '--no-pager', 'status', 'squeezelite'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise
        if resultat.returncode == 0:
            self.ids.resultatcommande.text = 'Success'
        else:
            self.ids.resultatcommande.text = 'Fail'
        #print(resultat)
        if resultat.stdout:
            lines = resultat.stdout.splitlines()
            self.ids.resultatcommande.text = str(resultat.stdout)
            #print('Sortie : ' + resultat.stdout)
        if resultat.stderr:
            lines = resultat.stderr.splitlines()
            self.ids.resultatcommande.text = str(resultat.stderr)
            #print('erreur : ' + resultat.stderr)

    def go_back(self):
        sm.current = "accueil"


class SqueezeliteSettingsWindow(Screen):

    def __init__(self, **kwargs):
        #self.buildLists()
        super(SqueezeliteSettingsWindow, self).__init__(**kwargs)

    def buildLists(self):
        liste_des_devices =  []
        result = subprocess.run(['squeezelite', '-l'], stdout=subprocess.PIPE)
        lines = result.stdout.splitlines()
        #print("data brutes A")
        #print(lines)
        #print(type(lines))

        for line in lines:
            lineliste = line.decode().split('-')
            linesimple = lineliste.pop(0)
            ligne_result = re.findall(r'.*=.*', linesimple)
            if ligne_result:
                liste_des_devices.append(linesimple)
        self.pickType = liste_des_devices
        #print(self.pickType)
        return (self.pickType)

    # For Spinner defining spinner clicked function
    def spinner_clicked(self, value):
        #print("Output selected is " + value)
        value = value.strip()
        les_lignes = ''
        fichier_conf = open('/etc/default/squeezelite', 'r')
        for line in fichier_conf:
            if 'SL_SOUNDCARD' in line:
                # skip the line in the new file rather comments the line
                line = line.replace('SL_SOUNDCARD', '#SL_SOUNDCARD')
                line = "SL_SOUNDCARD=" + '"' + value + '"' + '\n'

                self.ids.output_in_file.text += 'file configuration updated : ' + line + '\n'
            else:
                pass
            les_lignes = les_lignes + line
        fichier_conf.close()

        f = open('/etc/default/squeezelite', 'wt')
        f.write(les_lignes)
        f.close()

        # return self.text

    def clear(self):
        self.ids.a_b_param.text = ''
        self.ids.a_p_param.text = ''
        self.ids.a_f_param.text = ''
        self.ids.a_m_param.text = ''
        self.ids.param_close_output.text = ''
        self.ids.various_options.text = ''
        self.save()

        #notYetImplemented()

    def save(self):
        # sauver le fichier /etc/default/squeezelite avec les paramètres
        parametre = ''
        param_a_b = self.ids.a_b_param.text
        param_a_p = self.ids.a_p_param.text
        param_a_f = self.ids.a_f_param.text
        param_a_m = self.ids.a_m_param.text
        param_close_output = self.ids.param_close_output.text
        param_various_option = self.ids.various_options.text

        if param_a_b:
            parametre = '-a ' + param_a_b + ':' + param_a_p + ':' + param_a_f + ':' + param_a_m + ' '
            if param_various_option:
                #print( 'various option : ' + param_various_option)
                parametre += param_various_option
            else:
                #print ('no various options')
                pass
            if param_close_output:
                parametre += '-C ' + param_close_output
                #print(param_close_output)
            else:
                #print('no close output')
                pass
            les_lignes = ''
            fichier_conf = open('/etc/default/squeezelite', 'r')
            for line in fichier_conf:
                if 'SB_EXTRA_ARGS=' in line:
                    line = "SB_EXTRA_ARGS=" + '"' + parametre + '"' + '\n'
                    #self.ids.output_in_file.text = 'file configuration updated : ' + line
                else:
                    pass
                les_lignes = les_lignes + line
            fichier_conf.close()

            f = open('/etc/default/squeezelite', 'wt')
            f.write(les_lignes)
            f.close()
            self.ids.output_in_file.text += 'file configuration updated : ' + line + '\n'
        else:
            self.ids.output_in_file.text += 'No parameters, update and save... ' + '\n'
            les_lignes = ''
            fichier_conf = open('/etc/default/squeezelite', 'r')
            for line in fichier_conf:
                if 'SB_EXTRA_ARGS=' in line:
                    line = "#SB_EXTRA_ARGS=" + '\n'
                else:
                    pass
                les_lignes = les_lignes + line
            fichier_conf.close()

            f = open('/etc/default/squeezelite', 'wt')
            f.write(les_lignes)
            f.close()
            self.ids.output_in_file.text += 'file configuration updated : ' + line + '\n'



    def host_name(self):
        return socket.gethostname()

    def go_backBtn(self):
        sm.current = "accueil"

class DrivesWindow(Screen):

    class SelectableLabel(RecycleDataViewBehavior, Label):
        ''' Add selection support to the Label '''
        index = None
        selected = BooleanProperty(False)
        selectable = BooleanProperty(True)

        def refresh_view_attrs(self, rv, index, data):
            ''' Catch and handle the view changes '''
            self.index = index
            return super( ).refresh_view_attrs(
                rv, index, data)

        # me souviens plus où j'ai piqué ce truc qui ne fonctionne pas
        def on_touch_down(self, touch):
            ''' Add selection on touch down '''
            if super().on_touch_down(touch):
                return True
            if self.collide_point(*touch.pos) and self.selectable:
                return self.parent.select_with_touch(self.index, touch)

        def apply_selection(self, rv, index, is_selected):
            ''' Respond to the selection of items in the view. '''
            self.selected = is_selected

    class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
        """ Adds selection and focus behaviour to the view. """
        pass

    class RV(RecycleView):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.data = []
            self.show_mounted()
            #print(type(self.data))

        def show_mounted(self):
            self.data = []
            try:
                resultat_mount = subprocess.run(['mount'],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            except Exception as erreur:
                print(f"Unexpected {erreur=}, {type(erreur)=}")
                raise
            #print('passe 0')
            #print((type(resultat_mount)))
            if resultat_mount.stdout:
                lines = resultat_mount.stdout.splitlines()
                temp = str(resultat_mount.stdout)
                #print('Pass 1 ')
                #print(type(resultat_mount.stdout))
                #print('passe 1-2')
                #print('Sortie : ' + resultat_mount.stdout)
                for line in lines:
                    #self.data = self.data +
                    self.data = self.data + [{'text': line}]

                #    self.data =
            if resultat_mount.stderr:
                lines = resultat_mount.stderr.splitlines()
                temp = str(resultat_mount.stderr)
                #print('erreur : ' + resultat_mount.stderr)
                for line in lines:
                    #self.data = self.data +
                    self.data = self.data + [{'text': line}]

            #print(self.data)

    def clear(self):
        self.RV.data = []
        #print(self.RV.data)

    def show(self):
        #print('Drives.show')
        self.RV.show_mounted(self.RV)
        #print(self.RV.data)

    def attente(self):
        notYetImplemented()

    def go_back(self):
        sm.current = "accueil"

    def saveDrivesBtn(self):
        notYetImplemented()

class Drive_to_mountWindow(Screen):

    # Define scrollview class
    class ScrollableLabel(ScrollView):
        text = StringProperty('')

    def show_lsblk(self):

        try:
            # changelog : change command lsblk for blkid
            resultat_status = subprocess.run(['/usr/sbin/blkid'],
                                stdout=subprocess.PIPE,stderr=subprocess.PIPE, text=True)
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise
        #print(resultat_status.returncode)
        if resultat_status.stdout:
            lines = resultat_status.stdout.splitlines()
            lines_stdout_sorted = sorted(lines)
            #print(lines_stdout_sorted)
            string_device = ''
            for line in lines_stdout_sorted:
                string_device += line +'\n'
            self.ids.labelscrollable.text  = string_device
            #print('Sortie : ' + resultat_status.stdout)
        if resultat_status.stderr:
            lines = resultat_status.stderr.splitlines()
            self.ids.labelscrollable.text = str(resultat_status.stderr)
            #print('erreur : ' + resultat_status.stderr)

    def clear_lsblk(self):
        self.ids.labelscrollable.text = ''

    def save_cifs(self):
        mount_point_cifs = self.ids.mount_point_cifs.text
        #print((mount_point_cifs))
        ip_adresse = self.ids.ip_address_cifs.text
        #print(ip_adresse)
        share_name = self.ids.share_name_cifs.text
        #print(share_name)
        user_name_pass_option =''
        lignes_credential = ''
        if self.ids.username_cifs.text:
            lignes_credential =  'username=' + self.ids.username_cifs.text
        else:
            lignes_credential =  'username=guest'

        if self.ids.mot_de_passe_cifs.text:
            lignes_credential += '\npassword=' +  self.ids.mot_de_passe_cifs.text + '\n'

        if lignes_credential:
            fichier_credential = open('/home/user/.cred_file', 'w')
            fichier_credential.write(lignes_credential)
            fichier_credential.close()

        if self.ids.option_sup_cifs.text:
            user_name_pass_option += ','
            user_name_pass_option += self.ids.option_sup_cifs.text
        entree_autofs = ''
        if ip_adresse and share_name and mount_point_cifs:
            entree_autofs = mount_point_cifs + ' -fstype=cifs,credentials=/home/user/.cred_file,user=' + \
                  self.ids.username_cifs.text + ',uid=1000,gid=1000  ://' + ip_adresse + '/'+ share_name
        #print(entree_autofs)

        # following for memory but change code for autofs
        # format example of /etc/fstab :
        # CIFS =
        # 192.168.0.5/storage   /media/myname/TK-Public/   cifs  guest, uid = myuser, iocharset = utf8,  \
        #                                            file_mode = 0777, dir_mode = 0777, noperm   0   0
        #NFS =
        #192.168.0.1:/NASShare   /mnt/NAS  nfs  username = administrator, password = pass  0  0

        # following example of entry autofs smb :
        # montage -fstype=cifs,credentials=/home/user/.cred_file,user=john,uid=1000,gid=1000  :192.168.1.11/share
        # where :
        # uid et gid is the local id of the client owner of the montage - share mount point
        # 192.168.1.11 is the remote server
        # user john is the remote user to access share on the remote
        # user and password of john are in the file .cred_file
        self.ids.labelscrollable.text = 'Processing...\n'
        if entree_autofs:
            self.ids.entree_fichier_a_ecrire.text = entree_autofs
            self.ids.labelscrollable.text += ' To Do : mount point ' + '/cifs/' + mount_point_cifs +  '\n'
            self.ids.labelscrollable.text += ' To Do : Create entrée dans /etc/auto.cifs :  \n'
            #self.ids.labelscrollable.text += ' To Do : Mount the new entry :  \n'

            self.ids.labelscrollable.text += entree_autofs + '\n'
            self.ids.confirmation_cifs.text = 'Yes, I am sure. I agree to do it'
            self.ids.cancel_write.text = 'Non, je ne suis pas sûr(e) - Cancel '
            self.ids.confirmation_cifs.disabled = False
            self.ids.confirmation_cifs.background_color = (1,0,0,1)
            self.ids.cancel_write.disabled = False

        else:
            self.ids.labelscrollable.text += ' Nothing to do \n'
    ''' 
    Remplacer ce code par un montage AutoFS
        
    '''
    def confirmer_cifs(self):
        mount_point_cifs = self.ids.mount_point_cifs.text
        '''
        # echoue toujours car le répertoire /cifs  existe et monte avec autofs
        resultat_mkdir = subprocess.run(['sudo', 'mkdir', '/cifs'],
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.ids.labelscrollable.text += str(resultat_mkdir) + '\n'
        if resultat_mkdir.returncode == 0:
            self.ids.labelscrollable.text += '\nmkdir /cifs Success\n\n'
        else:
            self.ids.labelscrollable.text += '\nmkdir /cifs Fail\n'
            self.ids.confirmation.disabled = True
            self.ids.cancel_write.disabled = True
        '''
        resultat_cp = subprocess.run(['sudo', 'cp','-a', '/etc/auto.master.d/auto.cifs', '/etc/auto.master.d/auto.cifs.ori' ],
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        self.ids.labelscrollable.text += str(resultat_cp) +'\n'
        if resultat_cp.returncode == 0:
            self.ids.labelscrollable.text += '\nCopie sauvegarde auto.cifs en auto.cifs.ori Success !\n'
        else:
            self.ids.labelscrollable.text += " \nCopie de sauvegarde échouée , Fail, Sortie\n"
            self.ids.confirmation_cifs.disabled = True
            self.ids.cancel_write.disabled = True
            return
        ajout_autofs = self.ids.entree_fichier_a_ecrire.text + '\n'
        #print('ajout : ' + ajout_autofs)
        f = open('/etc/auto.master.d/autofs.ajout', 'wt')
        f.write(ajout_autofs)
        f.close()

        les_lignes_autofs = ''
        fichier_conf = open('/etc/auto.master.d/auto.cifs', 'r')
        for line in fichier_conf:
           les_lignes_autofs = les_lignes_autofs + line
        fichier_conf.close()
        les_lignes_autofs += ajout_autofs
        f = open('/etc/auto.master.d/auto.cifs', 'wt')
        f.write(les_lignes_autofs)
        f.close()

        self.ids.labelscrollable.text += les_lignes_autofs + '\n'
        self.ids.labelscrollable.text += '\nAjout entrée dans /etc/auto.master.d/auto.cifs :  À VERIFIER !\n'
        self.ids.confirmation_cifs.disabled = True
        self.ids.cancel_write.disabled = True
        self.ids.confirmation_cifs.text =''
        self.ids.cancel_write.text = ''
        return


    def cancel_write(self):
        self.ids.labelscrollable.text = 'Attente'
        self.ids.confirmation_cifs.disabled = True
        self.ids.confirmation_nfs.disabled = True
        self.ids.cancel_write.disabled = True
        self.ids.confirmation_cifs.text = ''
        self.ids.confirmation_nfs.text = ''
        self.ids.cancel_write.text = ''
        return

    def save_nfs(self):
        #notYetImplemented()
        mount_point_nfs = self.ids.mount_point_nfs.text
        print((mount_point_nfs))
        ip_adresse = self.ids.ip_address_nfs_server.text
        print(ip_adresse)
        share_name = self.ids.share_name_nfs_server.text
        print(share_name)

        entree_autofs = ''
        if ip_adresse and share_name and mount_point_nfs:
            if self.ids.option_nfs.text:
                entree_autofs = mount_point_nfs + '  -fstype=nfs,' + self.ids.option_nfs.text + ' ' + \
                              ip_adresse + ':/' + share_name
            else:
                entree_autofs = mount_point_nfs + '  -fstype=nfs  '  + ip_adresse + ':/' + share_name
        print(entree_autofs)

        self.ids.labelscrollable.text = 'Processing...\n'
        if entree_autofs:
            self.ids.entree_fichier_a_ecrire.text = entree_autofs
            self.ids.labelscrollable.text += ' To Do : mount point ' + '/net/' + mount_point_nfs + '\n'
            self.ids.labelscrollable.text += ' To Do : Create entrée dans /etc/auto.master.d/auto.nfs :  \n'

            self.ids.labelscrollable.text += entree_autofs + '\n'
            self.ids.confirmation_nfs.text = 'Yes, I am sure. I agree to do it'
            self.ids.cancel_write.text = 'Non, je ne suis pas sûr(e) - Cancel '
            self.ids.confirmation_nfs.disabled = False
            self.ids.confirmation_nfs.background_color = (1, 0, 0, 1)
            self.ids.cancel_write.disabled = False

        else:
            self.ids.labelscrollable.text += ' Nothing to do \n'

    def confirmer_nfs(self):
        mount_point_cifs = self.ids.mount_point_cifs.text
        resultat_cp = subprocess.run(['sudo', 'cp','-a', '/etc/auto.master.d/auto.nfs', '/etc/auto.master.d/auto.nfs.ori' ],
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        self.ids.labelscrollable.text += str(resultat_cp) +'\n'
        if resultat_cp.returncode == 0:
            self.ids.labelscrollable.text += '\nCopie sauvegarde auto.nfs en auto.nfs.ori Success !\n'
        else:
            self.ids.labelscrollable.text += " \nCopie de sauvegarde échouée , Fail, Sortie\n"
            self.ids.confirmation_nfs.disabled = True
            self.ids.cancel_write.disabled = True
            return
        ajout_autofs = self.ids.entree_fichier_a_ecrire.text + '\n'
        print('ajout : ' + ajout_autofs)
        f = open('/etc/auto.master.d/autofs_nfs.ajout', 'wt')
        f.write(ajout_autofs)
        f.close()

        les_lignes_autofs = ''
        fichier_conf = open('/etc/auto.master.d/auto.nfs', 'r')
        for line in fichier_conf:
           les_lignes_autofs = les_lignes_autofs + line
        fichier_conf.close()
        les_lignes_autofs += ajout_autofs
        f = open('/etc/auto.master.d/auto.nfs', 'wt')
        f.write(les_lignes_autofs)
        f.close()

        self.ids.labelscrollable.text += les_lignes_autofs + '\n'
        self.ids.labelscrollable.text += '\nAjout entrée dans /etc/auto.master.d/auto.nfs :  À VERIFIER !\n'
        self.ids.confirmation_nfs.disabled = True
        self.ids.cancel_write.disabled = True
        self.ids.confirmation_nfs.text =''
        self.ids.cancel_write.text = ''
        return

    def stop(self):
        notYetImplemented()

    def go_back(self):
        self.ids.labelscrollable.text = ''
        sm.current = "drives"




class LMSWindow(Screen):
    status = StringProperty()

    def go_back(self):
        self.ids.status.text = ''
        sm.current = "accueil"

    def statusBtn(self):
        try:
            resultat_status = subprocess.run(['sudo', 'systemctl', '--no-pager', 'status',
                                              'lyrionmusicserver'],
                                stdout=subprocess.PIPE,stderr=subprocess.PIPE, text=True)
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise
        if resultat_status.returncode == 0:
            self.ids.status.text = "Success"
        else:
            self.ids.status.text = "Fail"

        if resultat_status.stdout:
            lines = resultat_status.stdout.splitlines()
            self.ids.status.text = str(resultat_status.stdout)
            #print('Sortie : ' + resultat_status.stdout)
        if resultat_status.stderr:
            lines = resultat_status.stderr.splitlines()
            self.ids.status.text = str(resultat_status.stderr)
            #print('erreur : ' + resultat_status.stderr)

    def enable(self):
        try:
            resultat_status = subprocess.run(['sudo', 'systemctl','--no-pager', 'enable',
                                              'lyrionmusicserver'],
                                    stdout=subprocess.PIPE,stderr=subprocess.PIPE, text=True)
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise
        if resultat_status.returncode == 0:
            self.ids.status.text = "Enable : Success"
        else:
            self.ids.status.text = "Enable : Fail"
        if resultat_status.stdout:
            lines = resultat_status.stdout.splitlines()
            self.ids.status.text = str(resultat_status.stdout)
            #print('Sortie : ' + resultat_status.stdout)
        if resultat_status.stderr:
            #print('erreur : ' + resultat_status.stderr)
            lines = resultat_status.stderr.splitlines()
            #print(lines)
            self.ids.status.text = str(resultat_status.stderr)
            #print('erreur : ' + resultat_status.stderr)

    def disable(self):
        try:
            resultat_status = subprocess.run(['sudo', 'systemctl','--no-pager', 'disable',
                                              'lyrionmusicserver'],
                                    stdout=subprocess.PIPE,stderr=subprocess.PIPE, text=True)
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise
        if resultat_status.returncode == 0:
            self.ids.status.text = "Disable : Success"
        else:
            self.ids.status.text = "Disable : Fail"
        if resultat_status.stdout:
            lines = resultat_status.stdout.splitlines()
            self.ids.status.text = str(resultat_status.stdout)
            #print('Sortie : ' + resultat_status.stdout)
        if resultat_status.stderr:
            #print('erreur : ' + resultat_status.stderr)
            lines = resultat_status.stderr.splitlines()
            #print(lines)
            self.ids.status.text = str(resultat_status.stderr)
            #print('erreur : ' + resultat_status.stderr)

    def start(self):
        try:
            resultat_status = subprocess.run(['sudo', 'systemctl','--no-pager', 'start',
                                              'lyrionmusicserver'],
                                    stdout=subprocess.PIPE,stderr=subprocess.PIPE, text=True)
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise
        if resultat_status.returncode == 0:
            self.ids.status.text = "Start : Success"
        else:
            self.ids.status.text = "Start : Fail"
        if resultat_status.stdout:
            lines = resultat_status.stdout.splitlines()
            self.ids.status.text = str(resultat_status.stdout)
            #print('Sortie : ' + resultat_status.stdout)
        if resultat_status.stderr:
            #print('erreur : ' + resultat_status.stderr)
            lines = resultat_status.stderr.splitlines()
            #print(lines)
            self.ids.status.text = str(resultat_status.stderr)
            #print('erreur : ' + resultat_status.stderr)

    def stop(self):
        try:
            resultat_status = subprocess.run(['sudo', 'systemctl','--no-pager', 'stop', 'lyrionmusicserver'],
                                    stdout=subprocess.PIPE,stderr=subprocess.PIPE, text=True)
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise
        if resultat_status.returncode == 0:
            self.ids.status.text = " Stop : Success"
        else:
            self.ids.status.text = "Stop : Fail"

        if resultat_status.stdout:
            lines = resultat_status.stdout.splitlines()
            self.ids.status.text = str(resultat_status.stdout)
            #print('Sortie : ' + resultat_status.stdout)
        if resultat_status.stderr:
            lines = resultat_status.stderr.splitlines()
            self.ids.status.text = str(resultat_status.stderr)
             #print('erreur : ' + resultat_status.stderr)


class AboutWindow(Screen):

    def aboutBtn(self):
        notYetImplemented()

    def go_backBtn(self):
        sm.current = "accueil"

class HelpWindow(Screen):

    def aboutBtn(self):
        notYetImplemented()

    def go_backBtn(self):
        sm.current = "accueil"

class MainWindow(Screen):
    accueil = ObjectProperty(None)


    def logOut(self):
        sm.current = "accueil"

    def on_enter(self, *args):
        pass

    # pour un test mais ne semble pas fonctionner
    # à approfondir
    def on_key_down(self, window, keycode, text, modifiers, is_repeat, *args):
        if Keyboard.keycodes['X'] == keycode:
            exit()
        elif Keyboard.keycodes['A'] == keycode:
            sm.current = "About"
        elif Keyboard.keycodes['S'] == keycode:
            sm.current = "squeezelite"
        elif Keyboard.keycodes['D'] == keycode:
            sm.current = "drives"


class WindowManager(ScreenManager):
    pass


def notYetImplemented():
    pop = Popup(title='Sorry, Not Yet Implemented',
                  content=Label(text='In the next release, may be\n if you write it ...'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()

kv = Builder.load_file("controlpanelscreen.kv")

sm = WindowManager()

screens = [HelpWindow(name="help"),AboutWindow(name="about"),SqueezeliteStatWindow(name="squeezeliteStat"),
            SqueezeliteSettingsWindow(name="settingsSqueeze"), DrivesWindow(name="drives"),
            Drive_to_mountWindow(name="drive_to_mount"), LMSWindow(name="lyrion"), MainWindow(name="accueil")]

for screen in screens:
    sm.add_widget(screen)

sm.current = "accueil"


class controlpanelApp(App):

    def _on_keyboard_handler(self, instance, key, *args):
        #print('Keyboard pressed {}'.format(key))
        #print('key: ' + str(key))
        if key == 283: #F2
            sm.current = "help"
        elif key == 278 or key == 263:# Home
            sm.current = "accueil"
        elif key == 285: #F4
            sm.current = "squeezeliteStat"
        elif key == 286: #F5
            sm.current = "settingsSqueeze"
        elif key == 287: #F6
            sm.current = 'drives'
        elif key == 288: #F7
            sm.current = "lyrion"
        elif key == 289: #F8
            sm.current = "about"
        elif key == 289: #F9
            exit()

        else :
            pass


    def build(self):
        Window.bind(on_keyboard=self._on_keyboard_handler)
        return sm


if __name__ == "__main__":
    controlpanelApp().run()
