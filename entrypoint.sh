#!/bin/bash
set -e
cd /build

repo_full=$(cat ./repo)
repo_owner=$(echo $repo_full | cut -d/ -f1)
repo_name=$(echo $repo_full | cut -d/ -f2)
sed -i '/\[community\]/d' /etc/pacman.conf
sed -i 's/#ParallelDownloads = 5/ParallelDownloads = 5/' /etc/pacman.conf
pacman-key --init
pacman -Syu --noconfirm --needed sudo git base-devel wget
useradd builduser -m
chown -R builduser:builduser /build
git config --global --add safe.directory /build
sudo -u builduser gpg --keyserver keyserver.ubuntu.com --recv-keys 38DBBDC86092693E
passwd -d builduser
printf 'builduser ALL=(ALL) ALL\n' | tee -a /etc/sudoers

cat ./gpg_key | base64 --decode | gpg --homedir /home/builduser/.gnupg --import
rm ./gpg_key

for i in "linux-x13s" "mutter" "alsa-ucm-conf-git-x13s" "linux-x13s-archiso" "linux-x13s-rc" "mesa-a690" "x13s-firmware" "x13s-touchscreen-udev" ; do
	status=13
	git submodule update --init $i
	cd $i

	# mesa needs Dylan Baker/Eric Engestrom keys
	echo $i
	if [ $i == "mesa-a690" ]; then
		gpg --homedir /home/builduser/.gnupg --recv-keys 4C95FAAB3EB073EC
		gpg --homedir /home/builduser/.gnupg --recv-keys 8D8E31AFC32428A6
	fi

	for i in $(sudo -u builduser makepkg --packagelist); do
		package=$(basename $i)
		wget https://github.com/$repo_owner/$repo_name/releases/download/packages/$package \
			&& echo "Warning: $package already built, did you forget to bump the pkgver and/or pkgrel? It will not be rebuilt."
	done
	sudo -u builduser bash -c 'export MAKEFLAGS=-j$(nproc) && makepkg --sign -s --noconfirm'||status=$?

	# Package already built is fine.
	if [ $status != 13 ]; then
		exit 1
	fi
	cd ..
done

cp */*.pkg.tar.* ./
repo-add --sign ./$repo_owner-x13s.db.tar.gz ./*.pkg.tar.xz

for i in *.db *.files; do
cp --remove-destination $(readlink $i) $i
done
