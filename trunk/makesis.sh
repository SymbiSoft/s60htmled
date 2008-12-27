#!/bin/bash
VERSION='0.7.1'
# make distro
rm -rf build
mkdir -p build
cp utils.py build/
cp s60htmled.py build/default.py
# create sis-file
../Ensymble/ensymble.py py2sis --uid=0xe3e34da2 --appname="S60 HTML Editor" --shortcaption="HTMLEd" --version=$VERSION --vendor="D.Mych" --verbose build s60htmled-${VERSION}.sis
rm -rf build
