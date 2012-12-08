#!/bin/bash -e
[ -e "$1" ] && [ -n "$2" ] || { echo "Usage: $0 full-tarball date" >&2; exit 0; }
oldname="$1"
date="$2"
name="linux-firmware-free-$date"
name_nonfree="linux-firmware-nonfree-$date"
rm -rf "$name" "$name_nonfree"
mkdir "$name" "$name_nonfree"
tar -xf "$1" --strip-components=1 -C "$name_nonfree"

driver=
free=
files=
license=
cd $name_nonfree

cp -a WHENCE GPL* "../$name"

cat WHENCE | while read line; do
	set -e
	case "$line" in
	"Driver: "*)
		driver="${line#Driver: }"
		free=
		files=
		license=
		;;
	"File: "*)
		files="$files ${line#File: }"
		;;
	"Source: "*)
		free=1
		files="$files ${line#Source: }"
		;;
	"License: "*|"Licence: "*)
		license="${line#Licen?e: }"
		case "$license" in
		*"Allegedly"*|*"no source visible"*)
			;;
		*"GPL"*)
			free=1
			;;
		esac
		;;
	"Original licence information: None")
		free=
		;;
	"------"*)
		if [ -n "$free" ]; then
			echo "Including: $driver ($license)"
			for file in $files; do
				mkdir -p "../$name/$(dirname "$file")"
				mv "$file" "../$name/$(dirname "$file")"
			done
		else
			echo "Skipping: $driver ($license)"
		fi
		driver=
		;;
	esac
done
cd ..
tar -cJf $name.tar.xz $name
tar -cJf $name_nonfree.tar.xz $name_nonfree
rm -rf "$name" "$name_nonfree"
