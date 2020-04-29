name=$(cat *.spec | grep -i Name: | awk '{print $NF}')
repo_url=$(cat *.spec | grep -i Url: | awk '{print $NF}')
git clone --depth 1 git://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git $name
cd $name
git archive --format=tar --prefix $name-$(date +%Y%m%d)/ HEAD | zstd --ultra -22 > ../$name-$(date +%Y%m%d).tar.zst
cd -
