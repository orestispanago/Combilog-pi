# Combilog-pi

Read data from Friedrichs Combilog 1022 datalogger and upload to FTP + SFTP.

Using [combilog](https://github.com/theendlessriver13/combilog) library. 

* Records since last readout are retrieved from the datalogger.

* Records are grouped by date and saved as daily ```.csv``` files.

* The ```.csv``` files are uploaded to FTP and SFTP servers.


## Instructions

Edit the FTP and SFTP parameters in ```main.py```

Add your ```known_hosts``` file for the SFTP server connection.

To avoid overlapping cron job execution, use ```flock``` in crontab:

```
*/5 * * * * /usr/bin/flock -w 0 ~/combilog_pi.lock python3 ~/Combilog-pi/main.py
```

To check if your cron job is running:

```
grep CRON /var/log/syslog
```

To make sure that ```flock``` works:

```
flock -n -x ~/flock_file.lock true || echo "LOCKED"
```