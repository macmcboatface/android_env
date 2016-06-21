#!/bin/bash
grep -e "$1" -r -o * | uniq | sort
