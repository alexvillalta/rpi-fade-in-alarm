#!/bin/bash
 
curl wttr.in/${1:-""}?format="The+weather+in+%l+is+%C+with+a+temperature+of+%t,+humidity+of+%h,+and+wind+speed+of+%w\n" | gtts-cli -f - | mpg123 -f -10000 -