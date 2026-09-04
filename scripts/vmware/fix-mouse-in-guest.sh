#!/usr/bin/env bash
set -e
echo "kali" | sudo -S mkdir -p /etc/X11/xorg.conf.d

echo "kali" | sudo -S tee /etc/X11/xorg.conf.d/20-vmware.conf > /dev/null << 'EOF'
Section "Device"
    Identifier "VMware SVGA"
    Driver "vmware"
    Option "HWCursor" "off"
EndSection
EOF

echo "kali" | sudo -S tee /etc/X11/xorg.conf.d/20-modesetting.conf > /dev/null << 'EOF'
Section "Device"
    Identifier "Modesetting Video"
    Driver "modesetting"
    Option "SWcursor" "on"
EndSection
EOF

echo "kali" | sudo -S systemctl restart lightdm || true
