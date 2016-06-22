#!/bin/bash
echo "setting a few enviroment variables..."


export ENV_ROOT="/home/$USER/android_env" 

echo "ENV_ROOT=$ENV_ROOT"

export ANDROID_NDK_HOME=$ENV_ROOT/tools/toolchains/ndks/android-ndk-r10e
export ANDROID_NDK_ROOT=$ANDROID_NDK_HOME
export ANDROID_SDK_HOME=$ENV_ROOT/tools/toolchains/sdks/android-sdk-linux
export ANDROID_SDK_ROOT=$ANDROID_SDK_HOME
export JAVA_HOME=$ENV_ROOT/tools/toolchains/jdks/jdk1.8.0_91/

export SCRIPTS_ROOT=$ENV_ROOT/scripts
export TOOLS_ROOT=$ENV_ROOT/tools
export UTILS_ROOT=$ENV_ROOT/scripts/utils
export SMALI_SCRIPTS_ROOT=$SCRIPTS_ROOT/smali
export MISC_SCRIPTS_PATH=$ENV_ROOT/misc

echo "setting git repo paths"
export FRIDA_PATH=$TOOLS_ROOT/dynamic/frida
export SMALI_PATH=$TOOLS_ROOT/static/smali
export JADX_PATH=$TOOLS_ROOT/static/jadx
export LOBOTOMY_PATH=$TOOLS_ROOT/dynamic/lobotomy
export DEX2JAR_PATH=$TOOLS_ROOT/static/dex2jar
export APKTOOL_PATH=$TOOLS_ROOT/static/Apktool
export PYSIDE_SETUP_PATH=$TOOLS_ROOT/utils/pyside-setup
export PROTOD_PATH=$TOOLS_ROOT/static/Protod
export PROTOBUF_PATH=$TOOLS_ROOT/static/protobuf
export BINWALK_PATH=$TOOLS_ROOT/static/binwalk

export PROTOBUF_DISSECTOR_PATH=~/.wireshark/plugins/protobuf_dissector

export ANDROID_STUDIO_HOME=$TOOLS_ROOT/ides/android-studio/

#path mangling
export PATH=$PATH:$ANDROID_NDK_HOME
export PATH=$PATH:$ANDROID_STUDIO_HOME/bin
export PATH=$PATH:$ANDROID_SDK_HOME/tools
export PATH=$PATH:$TOOLS_ROOT
export PATH=$PATH:$UTILS_ROOT
export PYTHONPATH=$PYTHONPATH:$SCRIPTS_ROOT
export PATH=$PATH:$SCRIPTS_ROOT
export PATH=$PATH:$SMALI_SCRIPTS_ROOT
export PATH=$PATH:$MISC_SCRIPTS_PATH

echo "setting up aliases for external tools"
export APKTOOL_JAR_PATH=$TOOLS_ROOT/binaries/apktool.jar
alias apktool="java -jar $APKTOOL_JAR_PATH"

echo "setting up aliases for my stuff"
export TETHERING_SCRIPT_PATH=$SCRIPTS_ROOT/setup/tether.sh
alias tether="$TETHERING_SCRIPT_PATH"
export PROXIFYING_SCRIPT_PATH=$SCRIPTS_ROOT/setup/proxy.sh
alias proxify="$PROXIFYING_SCRIPT_PATH"

export ENV_PYTHON_VIRTUALENV=$ENV_ROOT/.virtualenv

export RELEASE_KEYSTORE=$ENV_ROOT/resources/my-release-key.keystore
export KEYSTORE_ALIAS="my-key-alias"
