#!/bin/sh
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

# Biblioteca de funciones de scripts
if [ -f /etc/init.d/functions ] 
    then
	. /etc/init.d/functions
elif [ -f /etc/rc.d/init.d/functions ] 
    then
	. /etc/rc.d/init.d/functions
else
	exit 0
fi

# Los siguientes parametros deben de configurarse segn el demonio
DAEMON=dialerd
PROGRAMA="Issabel Dialer"
DIR_TRABAJO=/opt/issabel/dialer
USUARIO=asterisk

# Los siguientes parametros son normalmente derivados de los dos primeros
SERVICE_LOCK="/var/lock/subsys/issabeldialer"
PIDFILE_USER="$DIR_TRABAJO/$DAEMON.pid"
PIDFILE_SYSTEM="/var/run/$DAEMON.pid"

start() {
    echo -n $"Starting $PROGRAMA: "
    NEWLANG=$LANG
    if [ "$LANG" == "tr_TR" -o "$LANG" == "tr_TR.UTF-8" ] ; then
        NEWLANG=en_US.UTF-8
    fi
    daemon $"su $USUARIO -c \"LANG=$NEWLANG $DIR_TRABAJO/$DAEMON\""
        RETVAL=$?
    echo
    if [ $RETVAL = 0 ] ; then
        touch $SERVICE_LOCK
        [ -f $PIDFILE_USER ] && cp $PIDFILE_USER /var/run/
    fi
}

stop () {
    echo -n $"Stopping $PROGRAMA: "
    killproc -d 20 $DAEMON
    RETVAL=$?
    echo
    if [ $RETVAL = 0 ] ; then
        rm -f $SERVICE_LOCK
        rm -f $PIDFILE_SYSTEM
    fi
}


restart() {
    stop
    start
}

case $1 in
	start)
		start
	;;
	stop)
		stop
	;;
	restart)
		restart
	;;
	condrestart)
		[ -f $SERVICE_LOCK ] && restart || :
	;;
	status)
		status $DAEMON
	;;
	*)

	echo $"Uso: $prog {start|stop|restart|condrestart|status}"
	exit 1
esac

exit $RETVAL
