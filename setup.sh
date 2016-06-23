#!/bin/bash
source ./env.sh
ANDROID_NDK_DOWNLOAD_PATH="http://dl.google.com/android/repository/android-ndk-r10e-linux-x86_64.zip"
ANDROID_SDK_DOWNLOAD_PATH="https://dl.google.com/android/android-sdk_r24.4.1-linux.tgz"
JDK_DOWNLOAD_PATH="http://download.oracle.com/otn-pub/java/jdk/8u91-b14/jdk-8u91-linux-x64.tar.gz"

SMALI_DOWNLOAD_PATH="https://bitbucket.org/JesusFreke/smali/downloads/smali-2.1.2.jar"
BAKSMALI_DOWNLOAD_PATH="https://bitbucket.org/JesusFreke/smali/downloads/baksmali-2.1.2.jar"
APKTOOL_DOWNLOAD_PATH="https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.1.1.jar"

function install_core_packages {
	echo "[+] Installing core packages"
	sudo apt-get install autogen 
	sudo apt-get install autoconf
	sudo apt-get install build-essential curl git python-setuptools ruby
	sudo apt-get install build-essential git cmake libqt4-dev libphonon-dev python2.7-dev libxml2-dev libxslt1-dev qtmobility-dev libqtwebkit-dev python-lzma
	sudo apt-get install autoconf automake libtool curl make g++ unzip
	sudo apt-get install build-essential libtool
	sudo apt-get install openjdk-8-jdk
	sudo ln -s /usr/bin/nodejs /usr/bin/node
}

function setup_python_env {
	echo "[+] Setting python env"
	echo "[+] Installing virtualenv"
	sudo pip install virtualenv
	sudo pip install virtualenv --upgrade

	echo "[+] Setup virtual env"
	virtualenv $ENV_PYTHON_VIRTUALENV
	source $ENV_PYTHON_VIRTUALENV/bin/activate
	pip install protobuf
	pip install protobuf --upgrade
	pip install ipython	
}

function install_toolchains {
	echo "[+] Install toolchain"
	if [ ! -d "$ANDROID_NDK_HOME" ]; then
		echo "[+] Setting Android NDK"
		ANDROID_NDK_ZIP=$(basename $ANDROID_NDK_DOWNLOAD_PATH)
		mkdir -p $TOOLCHAINS/ndks
		cd $TOOLCHAINS/ndks
		wget $ANDROID_NDK_DOWNLOAD_PATH 
		unzip $ANDROID_NDK_ZIP
		rm $ANDROID_NDK_ZIP
	fi

	if [ ! -d "$ANDROID_SDK_HOME" ]; then
		echo "[+] Setting Android SDK"
		ANDROID_SDK_ZIP=$(basename $ANDROID_SDK_DOWNLOAD_PATH)
		mkdir -p $TOOLCHAINS/sdks
		cd $TOOLCHAINS/sdks
		wget $ANDROID_SDK_DOWNLOAD_PATH 
		tar xzf $ANDROID_SDK_ZIP
		rm $ANDROID_SDK_ZIP
	fi 
}

function download_and_install_jar_tool {
	TOOLNAME="$1"
	DOWNLOAD_PATH="$2"
	BIN_NAME=$(basename $DOWNLOAD_PATH)
	TOOL_PATH="$TOOLS/$TOOLNAME"	
	mkdir -p $TOOL_PATH/bin
	cd $TOOL_PATH/bin
	if [ ! -f "$BIN_NAME" ] 
	then 
		echo "[+] Installing $TOOLNAME"
		wget $DOWNLOAD_PATH
		ln -s "$TOOL_PATH/bin/$BIN_NAME" "$TOOL_PATH/$TOOLNAME.jar"
		ln -s "$JAR_EXEC" "$TOOLS/bin/$TOOLNAME"
	fi
}

function clone_or_pull {
	REMOTE_PATH="$1"
	LOCAL_PATH="$2"
	if [ -d "$LOCAL_PATH" ] 
	then 
		cd "$LOCAL_PATH"
		git pull
	else
		git clone "$REMOTE_PATH" "$LOCAL_PATH"
		cd "$LOCAL_PATH"
	fi
}

function install_python_from_source {
	TOOLNAME="$1"
	GIT_REMOTE_PATH="$2"
	TOOL_PATH="$TOOLS/$TOOLNAME"
	SOURCE_PATH="$TOOL_PATH/source"
	clone_or_pull "$GIT_REMOTE_PATH" "$SOURCE_PATH"
	python setup.py install
}

function install_jadx {
	SOURCE_PATH="$TOOLS/jadx/source"
	clone_or_pull "https://github.com/skylot/jadx.git" "$SOURCE_PATH"
	cd $SOURCE_PATH
	./gradlew dist
	ln -s "$SOURCE_PATH/build/jadx/bin/jadx" "$TOOLS/bin/jadx"
	ln -s "$SOURCE_PATH/build/jadx/bin/jadx-gui" "$TOOLS/bin/jadx-gui"
}

function install_enjarify {
	SOURCE_PATH="$TOOLS/enjarify/source"	
	clone_or_pull "https://github.com/google/enjarify.git" "$SOURCE_PATH"
	mkdir -p "$TOOLS/enjarify/bin"
	ln -s "$SOURCE_PATH/enjarify.sh" "$TOOLS/bin/enjarify"
}

function install_tools {
	echo "[+] Installing tools"
	download_and_install_jar_tool smali "$SMALI_DOWNLOAD_PATH"
	download_and_install_jar_tool baksmali "$BAKSMALI_DOWNLOAD_PATH"
	download_and_install_jar_tool apktool "$APKTOOL_DOWNLOAD_PATH"
	install_python_from_source binwalk "https://github.com/devttys0/binwalk.git"
	pip install frida --upgrade 
	install_jadx
	install_enjarify
}

function prepare_paths {
	mkdir -p "$TOOLS/bin"
	mkdir -p "$SCRIPTS"
	mkdir -p "$TOOLCHAINS"
}

function install_all {
	CURRENT_DIR=$(pwd)
	prepare_paths
	install_core_packages
	setup_python_env		
	install_toolchains
	install_tools
	cd $CURRENT_DIR
}