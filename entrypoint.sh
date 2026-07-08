#!/bin/bash
set -e
cd /build


repo_full=$(cat ./repo)
repo_owner=$(echo $repo_full | cut -d/ -f1)
repo_name=$(echo $repo_full | cut -d/ -f2)
echo "Repo owner: $repo_owner"
echo "Repo name $repo_name"
exit 1
sed -i '/\[community\]/d' /etc/pacman.conf
sed -i 's/#ParallelDownloads = 5/ParallelDownloads = 5/' /etc/pacman.conf
pacman-key --init
pacman -Sy --noconfirm archlinux-keyring
pacman -Syu --noconfirm --needed sudo git wget python
useradd builduser -m
chown -R builduser:builduser /build
git config --global --add safe.directory /build
sudo -u builduser gpg --recv-keys 38DBBDC86092693E
passwd -d builduser
printf 'builduser ALL=(ALL) ALL\n' | tee -a /etc/sudoers

cat ./gpg_key | base64 --decode | gpg --homedir /root/.gnupg --import
cat ./gpg_key | base64 --decode | gpg --homedir /home/builduser/.gnupg --import
rm ./gpg_key
echo "checking out buildusers key"
gpg --homedir /home/builduser/.gnupg --list-keys
echo "checking out root key"
gpg --homedir /root/.gnupg --list-keys

sudo pacman -S aarch64-linux-gnu-binutils aarch64-linux-gnu-gcc base-devel  --noconfirm --needed

for i in "linux-x13s" "archinstall-x13s" ; do
	status=13
	git submodule update --init $i
	cd $i

	for i in $(sudo -u builduser makepkg --packagelist); do
		package=$(basename $i)
		wget https://github.com/$repo_owner/$repo_name/releases/download/packages/$package \
			&& echo "Warning: $package already built, did you forget to bump the pkgver and/or pkgrel? It will not be rebuilt."
	done
	sudo -u builduser bash -c 'export MAKEFLAGS=-j"$(nproc)"; export CARCH=aarch64; makepkg --sign -s --noconfirm' || status=$?

	# Package already built is fine.
	if [ $status != 13 ]; then
		exit 1
	fi
	cd ..
done

cp */*.pkg.tar.* ./
gpg --list-keys
repo-add --sign ./$repo_owner-x13s.db.tar.gz ./*.pkg.tar.zst

for i in *.db *.files; do
cp --remove-destination $(readlink $i) $i
done
