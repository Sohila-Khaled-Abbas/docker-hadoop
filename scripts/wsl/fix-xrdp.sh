#!/usr/bin/env bash
set -e

echo "--> Applying complete xrdp + XFCE4 fix for Ubuntu 24.04..."

# 1. Configure /etc/xrdp/startwm.sh
cat << 'EOF' > /etc/xrdp/startwm.sh
#!/bin/sh
if test -r /etc/profile; then
    . /etc/profile
fi

unset DBUS_SESSION_BUS_ADDRESS
unset XDG_RUNTIME_DIR

export XDG_CURRENT_DESKTOP=XFCE
export XDG_DATA_DIRS=/usr/share/xfce4:/usr/local/share:/usr/share
exec startxfce4
EOF
chmod +x /etc/xrdp/startwm.sh

# 2. Configure port 3390 in xrdp.ini
sed -i 's/port=3389/port=3390/g' /etc/xrdp/xrdp.ini
if ! grep -q "port=3390" /etc/xrdp/xrdp.ini; then
    sed -i 's/port=.*/port=3390/g' /etc/xrdp/xrdp.ini
fi

# 3. Prevent colord crash in polkit
mkdir -p /etc/polkit-1/rules.d/
cat << 'EOF' > /etc/polkit-1/rules.d/45-allow-colord.rules
polkit.addRule(function(action, subject) {
    if (action.id.indexOf("org.freedesktop.color-manager.") === 0) {
        return polkit.Result.YES;
    }
});
EOF

# 4. User .xsession file
echo "startxfce4" > /home/hadoopuser/.xsession
chmod 644 /home/hadoopuser/.xsession
chown hadoopuser:hadoopuser /home/hadoopuser/.xsession

# 5. Add user to ssl-cert
adduser hadoopuser ssl-cert 2>/dev/null || true

# 6. Restart services
service xrdp-sesman restart
service xrdp restart

echo "--> xrdp services successfully restarted on port 3390!"
service xrdp status | head -n 10
