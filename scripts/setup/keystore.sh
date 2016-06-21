#!/bin/bash
source ../../env.sh
source ./env.sh
keytool -genkey -v -keystore $RELEASE_KEYSTORE -alias $KEYSTORE_ALIAS -keyalg RSA -keysize 2048 -validity 10000
