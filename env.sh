#!/bin/bash
export ENV_ROOT="/home/$USER/android_env" 
export SCRIPTS=$ENV_ROOT/scripts
export TOOLS=$ENV_ROOT/tools
export TOOLCHAINS=$ENV_ROOT/toolchains
export ANDROID_NDK_HOME=$TOOLCHAINS/ndks/android-ndk-r10e
export ANDROID_NDK_ROOT=$ANDROID_NDK_HOME
export ANDROID_SDK_HOME=$TOOLCHAINS/sdks/android-sdk-linux
export ANDROID_SDK_ROOT=$ANDROID_SDK_HOME
export JAVA_HOME="/usr/lib/jvm/default-java"

export JAR_EXEC=$ENV_ROOT/jarexec.sh
export UTILS_ROOT=$ENV_ROOT/scripts/utils
export SMALI_SCRIPTS=$SCRIPTS/smali
export MISC_SCRIPTS_PATH=$ENV_ROOT/misc

#path mangling
export PATH=$PATH:$ANDROID_NDK_HOME
export PATH=$PATH:$ANDROID_STUDIO_HOME/bin
export PATH=$PATH:$ANDROID_SDK_HOME/tools
export PATH=$PATH:$TOOLS/bin
export PATH=$PATH:$UTILS_ROOT
export PYTHONPATH=$PYTHONPATH:$SCRIPTS
export PATH=$PATH:$SCRIPTS
export PATH=$PATH:$SMALI_SCRIPTS
export PATH=$PATH:$MISC_SCRIPTS_PATH

# echo "setting up aliases for external tools"

export TETHERING_SCRIPT_PATH=$SCRIPTS/setup/tether.sh
alias tether="$TETHERING_SCRIPT_PATH"
export PROXIFYING_SCRIPT_PATH=$SCRIPTS/setup/proxy.sh
alias proxify="$PROXIFYING_SCRIPT_PATH"

export ENV_PYTHON_VIRTUALENV=$ENV_ROOT/.virtualenv

alias ash='adb shell'
alias alog='adb logcat -v threadtime'
alias alogc='adb logcat -c'
alias aglog='alog | grep'

# export RELEASE_KEYSTORE=$ENV_ROOT/resources/my-release-key.keystore
# export KEYSTORE_ALIAS="my-key-alias"
