#!/usr/bin/python
#
#   Script de inicio y finalización de un servicio de framework
#   de demonio de Palosanto Solutions, compatible con
#   sistema de inicio de servicios de RedHat/Fedora (chkconfig).
#   Este script asume que el servicio se inicia desde el comienzo
#   con privilegios de usuario normal (no root)
#
#   chkconfig: 2345 91 19
#   description: IssabelDialer
#

import os
import sys

# Biblioteca de funciones de scripts
if os.path.isfile('/etc/init.d/functions'):
    execfile('/etc/init.d/functions')
elif os.path.isfile('/etc/rc.d/init.d/functions'):
    execfile('/etc/rc.d/init.d/functions')
else:
    sys.exit(0)

# Los siguientes parametros deben de configurarse segn el demonio
DAEMON = 'dialerd'
PROGRAMA = 'Issabel Dialer'
DIR_TRABAJO = '/opt/issabel/dialer'
USUARIO = 'asterisk'

# Los siguientes parametros son normalmente derivados de los dos primeros
SERVICE_LOCK = '/var/lock/subsys/issabeldialer'
PIDFILE_USER = os.path.join(DIR_TRABAJO, DAEMON + '.pid')
PIDFILE_SYSTEM = '/var/run/' + DAEMON + '.pid'

def start():
    print('Starting ' + PROGRAMA + ': ', end='')
    NEWLANG = os.environ.get('LANG')
    if NEWLANG == 'tr_TR' or NEWLANG == 'tr_TR.UTF-8':
        NEWLANG = 'en_US.UTF-8'
    os.system('daemon "su ' + USUARIO + ' -c \\"LANG=' + NEWLANG + ' ' + os.path.join(DIR_TRABAJO, DAEMON) + '\\""')
    RETVAL = os.system('echo $?')
    print()
    if RETVAL == 0:
        open(SERVICE_LOCK, 'a').close()
        if os.path.isfile(PIDFILE_USER):
            os.system('cp ' + PIDFILE_USER + ' /var/run/')

def stop():
    print('Stopping ' + PROGRAMA + ': ', end='')
    os.system('killproc -d 20 ' + DAEMON)
    RETVAL = os.system('echo $?')
    print()
    if RETVAL == 0:
        os.remove(SERVICE_LOCK)
        os.remove(PIDFILE_SYSTEM)

def restart():
    stop()
    start()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Uso: ' + sys.argv[0] + ' {start|stop|restart|condrestart|status}')
        sys.exit(1)
    elif sys.argv[1] == 'start':
        start()
    elif sys.argv[1] == 'stop':
        stop()
    elif sys.argv[1] == 'restart':
        restart()
    elif sys.argv[1] == 'condrestart':
        if os.path.isfile(SERVICE_LOCK):
            restart()
    elif sys.argv[1] == 'status':
        os.system('status ' + DAEMON)
    else:
        print('Uso: ' + sys.argv[0] + ' {start|stop|restart|condrestart|status}')
        sys.exit(1)
    sys.exit(RETVAL)