#!/bin/sh
# /etc/init.d/lightshow_setup.sh

### BEGIN INIT INFO
# Provides:          something
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Simple script to start a program at boot
# Description:       A simple script from www.stuffaboutcode.com which will start / stop a program a boot / shutdown.
### END INIT INFO

# If you want a command to always run, put it here

# Carry out specific functions when asked to by the system
case "$1" in
  start)
    echo "Starting lightshow"
    # run application you want to start
    sh /home/pi/Public/lightshow/init_lights.sh
    ;;
  stop)
    echo "Stopping lightshow"
    # kill application you want to stop
    killall python
    ;;
  *)
    echo "Usage: /etc/init.d/lightshow_setup.sh {start|stop}"
    exit 1
    ;;
esac

exit 0
