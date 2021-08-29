This is a web interface for jbofihe, normally hosted at
https://jboski.lojban.org/ .  It is based loosely on the original
jboski, whose source (the PHP bits) is at
https://lojban.org/jboski/index.php.txt , and was written by Raphaël
Poss.

Most of what's in this repo is the container management code for
the site.  The actual code for the site, such as it is, is at
containers/web/src/ , but the heavy lifting is done by
https://github.com/lojban/jbofihe/

The container management code in this repo is an LBCS instance (see
https://github.com/lojban/lbcs/ ), which is why a bunch of things in
here are symlinks off into apparently empty space; you have to have
LBCS installed in /opt/lbcs/ for them to work.

That's also where the docs on how to start and stop the service and
so on are.
