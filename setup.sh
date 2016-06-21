#!/bin/bash
source ./env.sh
if [ "$1" == "install" ]
	then
		echo "install required packages"
		sudo apt-get install autogen
		sudo apt-get install autoconf
		#sudo apt-get install node
		#sudo apt-get install npm
		#sudo apt-get install python3-pip
		#sudo pip3 install colorama prompt-toolkit pygments
		#npm install frida
		sudo ln -s /usr/bin/nodejs /usr/bin/node
		sudo apt-get install build-essential curl git python-setuptools ruby
		sudo apt-get install build-essential git cmake libqt4-dev libphonon-dev python2.7-dev libxml2-dev libxslt1-dev qtmobility-dev libqtwebkit-dev
		sudo apt-get install autoconf automake libtool curl make g++ unzip
		sudo apt-get install build-essential libtool

		echo "installing virtualenv"
		sudo pip install virtualenv
		sudo pip install virtualenv --upgrade

		echo "clone git repos"
		git clone https://github.com/Linuxbrew/brew.git $LINUXBREW_PATH
		git clone https://github.com/JesusFreke/smali.git $SMALI_PATH
		git clone https://github.com/skylot/jadx.git $JADX_PATH
		git clone https://github.com/frida/frida.git $FRIDA_PATH
		git clone https://github.com/pxb1988/dex2jar.git $DEX2JAR_PATH
		git clone https://github.com/iBotPeaches/Apktool.git $APKTOOL_PATH
		git clone https://github.com/PySide/pyside-setup.git $PYSIDE_SETUP_PATH
		git clone https://github.com/google/protobuf.git $PROTOBUF_PATH
		git clone https://github.com/sysdream/Protod.git $PROTOD_PATH
		git clone https://github.com/devttys0/binwalk.git $BINWALK_PATH
		git clone https://github.com/128technology/protobuf_dissector.git $PROTOBUF_DISSECTOR_PATH

		echo "setup virtual env"
		virtualenv $ENV_PYTHON_VIRTUALENV
fi

source $ENV_PYTHON_VIRTUALENV/bin/activate

if [ "$1" == "install" ]
	then
		echo "installing pip packages"
		pip install frida
		pip install frida --upgrade
		pip install protobuf
		pip install protobuf --upgrade
		
	
		echo "installing binwalk"
		PWD=`pwd`
		cd $BINWALK_PATH
		python setup install
		cd $PWD

		#echo "building pyside for lobotomy"
		#PWD=`pwd`
		#cd $PYSIDE_SETUP_PATH
		#python setup.py bdist_wheel --qmake=/usr/bin/qmake-qt4 --version=1.2.4
		#pip install dist/PySide-1.2.4-cp27-none-linux-x86_64.whl
		#cd $PWD

		#echo "building dex2jar tools"
		#PWD=`pwd`
		#cd $DEX2JAR_PATH
		#./gradlew build
		#cd $PWD
		#ln -s $DEX2JAR_PATH/dex-tools/build/generated-sources/bin/d2j-apk-sign.sh $TOOLS_ROOT/d2j-apk-sign.sh
		#ln -s $DEX2JAR_PATH/dex-tools/build/libs $ $TOOLS_ROOT
		
		$SCRIPTS_ROOT/setup/keystore.sh
		
fi

#echo "pulling git updates"
#PWD=`pwd`
#cd $SMALI_PATH;git pull
#cd $JADX_PATH;git pull
#cd $FRIDA_PATH;git pull
#cd $DEX2JAR_PATH;git pull
#cd $PWD

