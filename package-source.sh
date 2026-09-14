TAG="$1"
if [ -z "$TAG" ]; then
	TAG=HEAD
	VER=$(date +%Y%m%d)
else
	VER=$TAG
fi
name=linux-firmware # $(cat *.spec | grep -i Name: | awk '{print $NF}')
repo_url=$(cat *.spec | grep -i Url: | awk '{print $NF}')
git clone -b $TAG --depth 1 git://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git $name
cd $name
git archive --format=tar --prefix $name-$VER/ $TAG | zstd --ultra -22 > ../$name-$VER.tar.zst
cd -
