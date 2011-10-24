s|^\([A-Z]*\) /[^\ ]*|\1 {path}|
s|^Host: .*$|Host: {host}|
s|^User-Agent: .*$|User-Agent: {agent}|
s|ISO-8859-2|{charset}|
s|hu-HU|{locale_upper}|
s|hu-hu|{locale_lower}|
s|hu|{language}|
