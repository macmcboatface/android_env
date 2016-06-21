#!/bin/bash
ifconfig | grep "Link encap" | cut -f1 -d ' '
