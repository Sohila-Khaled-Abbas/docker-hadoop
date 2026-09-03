#!/usr/bin/env bash
set -e

echo "================================================================="
echo "  🚀 Enabling Hyper-V Enhanced Session, Smooth Mouse & Clipboard  "
echo "================================================================="

# 1. Install Hyper-V integration tools and xrdp
sudo apt-get update -y
sudo apt-get install -y linux-tools-virtual linux-cloud-tools-virtual xrdp xorgxrdp

# 2. Stop xrdp to configure vsock transport
sudo systemctl stop xrdp
sudo systemctl stop xrdp-sesman

# 3. Configure xrdp for Hyper-V socket (HvSocket) transport
sudo sed -i_orig -e 's/port=3389/port=vsock:\/\/-1:3389/g' /etc/xrdp/xrdp.ini
sudo sed -i -e 's/use_vsock=false/use_vsock=true/g' /etc/xrdp/xrdp.ini 2>/dev/null || true
if ! grep -q "use_vsock" /etc/xrdp/xrdp.ini; then
    sudo sed -i '/\[Globals\]/a use_vsock=true' /etc/xrdp/xrdp.ini
fi
sudo sed -i -e 's/security_layer=negotiate/security_layer=rdp/g' /etc/xrdp/xrdp.ini
sudo sed -i -e 's/crypt_level=high/crypt_level=none/g' /etc/xrdp/xrdp.ini
sudo sed -i -e 's/bitmap_compression=true/bitmap_compression=true/g' /etc/xrdp/xrdp.ini

# 4. Enable bidirectional clipboard in sesman.ini
sudo sed -i -e 's/EnableClipboard=false/EnableClipboard=true/g' /etc/xrdp/sesman.ini
if ! grep -q "EnableClipboard=true" /etc/xrdp/sesman.ini; then
    sudo sed -i '/\[Sessions\]/a EnableClipboard=true' /etc/xrdp/sesman.ini
fi

# 5. Add user to ssl-cert
sudo adduser $USER ssl-cert 2>/dev/null || true

# 6. Start services
sudo systemctl daemon-reload
sudo systemctl enable --now xrdp
sudo systemctl restart xrdp-sesman
sudo systemctl restart xrdp

echo "================================================================="
echo "  🎉 Hyper-V Enhanced Session Configured Successfully!            "
echo "  Restart the VM to activate Full Screen, Smooth Mouse & Clipboard."
echo "================================================================="
