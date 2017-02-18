name=$(cat *.spec | grep -i Name: | awk '{print $NF}')
repo_url=$(cat *.spec | grep -i Url: | awk '{print $NF}')
git clone git://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git $name
pushd $name
git archive --format=tar --prefix $name-$(date +%Y%m%d)/ HEAD | xz -vf > ../$name-$(date +%Y%m%d).tar.xz
popd
