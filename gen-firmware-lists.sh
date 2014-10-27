#!/bin/bash -e
[ -e WHENCE ] || { echo "Usage: cd linux-firmware ; $0" >&2; exit 1; }
rm -f free.list nonfree.list
cat WHENCE | while read line; do
	set -e
	case "$line" in
	"Driver: "*)
		driver="${line#Driver: }"
		free=
		files=
		license=
		;;
	"File: "*|"sl: "*)
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
		if echo $files |grep -q radeon; then
			LIST=radeon
		elif echo $files | grep -qe iwlwifi -qe ibt-hw; then
			LIST=iwlwifi
		elif [ -n "$free" ]; then
			LIST=free
		else
			LIST=nonfree
		fi
		for file in $files; do
			[ -e $file ] && echo /lib/firmware/$file >>$LIST.list
		done
		echo "$LIST: $driver ($license)"
		driver=
		files=
		;;
	esac
done
