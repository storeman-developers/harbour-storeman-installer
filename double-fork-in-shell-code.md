# Double-fork in shell code

`(umask 0022; cd /; setsid --fork sh -c '(umask 0022; cd /; <command-list-to-execute [$1,$2,…]> [redirections-for-a-command]) > /dev/null 2>&1 < /dev/null &' <arbitrary-name-for-$0-"inside"-sh-c> <parameter1-for-$1-"inside"-sh-c> <parameter2-for-$2-"inside"-sh-c> …) > /dev/null 2>&1 < /dev/null`

This is the "generic form", the strictly static elements are the sequence:<br />
`setsid --fork sh -c '(<cmd-list>) &'`

## Variations
- The environment is copied down through the call chain with all shell implementations (as usual), *except* across the `setsid --fork sh -c ' '` sequence, for which a fresh default environment might be provided (e.g., when a different shell executable is called by setsid than the callers shell).<br />
  Hence the safe way to carry parameters across this sequence down the call chain are positional parameters, as described in the man-page of the shell of your choice for the option `-c`.<br />
  Also note that all shells must copy their environment to sub-shells opened with `( )` and commands run in a sub-shell (what most shells do for every shell-external command), additionally some shells also copy their regular variables (the ones not exported to the environment) down to sub-shells opened with `( )`, but this is implementation dependent.
- One can set the "inner" umask and PWD (via `cd`) as it fits best: The exemplary values in the "generic form" are just often used values; I often set the umask more restrictively.<br />
  Note that the directory to change into must exist (you do not want a `cd` at this point to fail), hence `/` is a safe value, as e.g., `/tmp` is not available early in the boot-phase (not relevant for actions triggered by a regular user).
- One sure can redirect from or to anywhere else than `/dev/null` or redirect StdIN and StdERR differently.
- With a proper POSIX-compliant shell, one can close any file descriptor with "&-", e.g., for StdIN `>&-`, instead of redirecting it from or to `/dev/null`.<br />
  But e.g., busybox's ash is not POSIX-compliant.<br />
  Also note that when closing StdOUT or StdERR, anything writing to a closed file descriptor will (/ might / should / must?  POSIX might tell.) fail, just as reading from a closed StdIN, in contrast to redirections to `/dev/null`.  This is fine if one ensures that the commands executed do not use any closed file descriptors.

## Notes
- It is strongly recommended to explicitly set StdIN, StdOUT and StdERR to known good values (or ensure that they are sane, already), both for the "outer" / topmost sub-shell and right "inside" the `sh -c ' '`, because they are part of the environment (which is then copied down further), as depicted in the "generic form" above.
- The innermost / bottom fork is only deemed necessary on System V descendent UNIXes, for the command-list being executed in a shell, which is *not* a session leader (see section "[Background](#background)" below).  Hence on BSD-UNIXes one may omit the innermost `(kill $PPID; <cmd-list>) &` and use `… setsid --fork sh -c '<cmd-list>' …` (or for a single command: `… setsid --fork <command> <arg1> <arg2> …`) instead.  Well, Linux is a System V UNIX by design, but all code is newly and independently written, in contrast to, e.g., HP-UX, IRIX, Sinix etc. (Solaris2?), which contain code from the original System V Release 4 ("SVR4").  I have not researched much, which property "System V descendent UNIX" addresses and how real the dangers are, because once the scheme of double-forking in shell code is understood, it is easy to perform another fork by `(kill $PPID; <cmd-list>) &`, so I went this way.
- For terminating a (sub-) shell via `SIGTERM`, this shell must not be an interactive shell (POSIX requires interactive shell instances to ignore a `SIGTERM`).  Thus for experimenting / testing in an interactive shell, one might wrap the whole "generic form" (or a variation of it) in another `sh -c ' '`.
- The caller of the "generic form" is terminated immediately after calling it.  One can think of other ways to ensure that execution of the original caller ends, e.g., see "[Larger variations](#larger-variations)", below.
- The outer and inner sub-shell must be started detached (by an appended ` &`), otherwise their parent would be stopped during the execution within that sub-shell, hence the caller would not be able to receive and handle the `SIGTERM` sent to it by `kill`.
- The explicit use of a sub-shell may be superfluous in some special cases: IMHO all shells start a single detached command (i.e., `<cmd> <args> <redirs> &`) automatically in a sub-shell, many execute all external commands in a sub-shell etc., but there may be cases in which this assumption will fall short.<br />
  Plus, expressing the execution in a sub-shell explicitly never does harm, improves readability (one does not have to know / think about the specific shell's automatisms) and enhances portability.
- Real double-forking / daemonising (including the "anti-session-leader extra-fork" for SysV-UNIXes) is impossible to achieve via `nohup <command> <args> <redirs> &` or `(<cmd-list>) & disown [-h] $!`
- Do check that the process hierarchy looks as it should (see section "[Background](#background)" below); the tree-view of GNU-`ps` (option `--forest`) or `pstree` are quite useful to see the hierarchical aspects much easier.  To observe the dynamics of these action and or short running, fully detached processes, this can be best achieved by instrumenting the calling and called script with `ps -o stat,tty,user,group,pgid,sid,ppid,pid,comm,args`, plus appropriate, not too tight filtering (e.g., `ps -eo … | grep …` etc.) and output redirection to a file (e.g., `>> mylog.txt`).  See [this branch for an example](https://github.com/storeman-developers/harbour-storeman-installer/tree/2.0.44), the minimalistic `ps` calls are used in order to be able to work with busybox's `ps` implementation (which is also not POSIX compliant).

## Larger variations
- Because one usually starts the whole double-fork to the innermost \<command-list\> or \<script-call\> from a shell (respectively, a script running in one), which is not intended to be terminated by an external trigger (here: from a detached shell process it just started), one can (ab)use the shell from which the double fork is called as first fork, if it is known to finish soon.  This has to checked for by the callee, thus it needs that PID to be handed down (specifically across the `setsid --fork sh -c ' '` sequence).  Hence one might use in the calling shell:
  ```
  …
  umask 0022
  [ "$PWD" = /tmp ] || cd /tmp  # Set PWD to /tmp
  setsid --fork sh -c '(kill $PPID; umask 0022; [ "$PWD" = /tmp ] || cd /tmp; <Wait for process with PID $1 to die>; <cmd-list [$2]> [redirs-for-a-cmd]) > /dev/null 2>&1 < /dev/null &' <name-for-$0> $$ <param2-for-$2> > /dev/null 2>&1 < /dev/null
  exit 0
  ```
  A "real-life example" [can be seen here](https://github.com/storeman-developers/harbour-storeman-installer/blob/2.0.45/bin/harbour-storeman-installer#L147).
- Because a long \<command-list\> "inside" the `sh -c ' '` is not nice to handle and maintain, one can simply put the \<command-list\> in a shell script (which might consume positional parameters) and call that via `setsid --fork sh -c '(myscript $1 $2 …) > /dev/null 2>&1 < /dev/null &' <name-for-$0> $$ <param2-for-$2> > /dev/null 2>&1 < /dev/null.  `myscript` should then perform the necessary actions, e.g. (continuing to use the example introduced one bullet point above):
  ```
  #!/bin/sh
  kill $PPID
  umask 0022
  [ "$PWD" = /tmp ] || cd /tmp  # Set PWD to /tmp
  <Wait for process with PID $1 to die>
  <cmd-list [$2]>
  …
  ```
  A "real-life example" [can be seen here](https://github.com/storeman-developers/harbour-storeman-installer/blob/2.0.45/bin/harbour-storeman-installer#L31) with the [\<Wait for process with PID $1 to die\>](https://github.com/storeman-developers/harbour-storeman-installer/blob/2.0.45/bin/harbour-storeman-installer#L55) further down in this shell script.

## Background
### My issue: To trigger the installation of an rpm from a scriptlet of another one
I had to trigger the installation of an rpm package from within an spec file scriptlet of an "installer" rpm package, for which the `%posttrans` scriptlet is the natural place, as it is run last.  Side note: In general this should not be necessary, my initial reaction also was "this is conceptually wrong and shall be handled by proper dependency definitions", but it turned out to be a special case with restrictions which do create a necessity for this; other workarounds would be much harder to deploy for an average user.  Here, the "installer" package has to enable an appropriate, dynamically determined repository (dependent on CPU-architecture, installed OS release etc.) in order to access the correct main package; before this repository is not enabled, i.e., before the installation of the "installer" package has not finished, resolving dependencies for a main package cannot be performed, because the (/ any) specific main package is not yet accessible.

I know that other people have solved this by utilising `cron` or `systemd`, but after having successfully [implemented this via an indirection by a systemd unit](https://github.com/storeman-developers/harbour-storeman-installer/tree/2.0.31/), I realised:
- The indirection via `cron` or `systemd` achieves that the started process is fully detached from the caller: I.e., that the caller is not an ancestor (parent, grandparent etc.) of the callee, plus that it is run within a different session (see `ps`'s field `sid` for the SessionID) and hence does not share a TTY with the caller, any longer.
- One does not want any time-based waiting, because no one can tell how long the initial "installer" package installation will take on a non-deterministic software stack (i.e., not a real-time system); imagine a machine is heavily swapping and hence (almost) grinding to a halt.  Thus timer units or cron jobs are not suitable to implement this robustly.
- Consequently one has to transmit the PID of the `%posttrans` scriptlet interpreter (usually `bash`) to the fully detached process, when it is instanciated, so it can wait for the `%posttrans` interpreter to finish execution of the scriptlet.  Systemd allows for a single parameter to be transmitted to "instanciated units", but the wait function (a `while` or `until` loop) has to be implemented in an external script called by an `ExecStartPre=` statement (or pack the whole wait function awkwardly in an `sh -c ' '`), because systemd does not allow for loops or any other kind of program flow control.
- That was the moment I realised that a single, own shell script is more elegant and provides one with many more degrees of freedom than being limited to systemd's unit syntax.  The only open design question was then how to become fully detached from the caller.  I remembered the concept of double-forking / "daemonizing" for UNIX daemons, which were once usually written in C, to fully detach a process from its caller.
- The final twist for a robust implementation was [to trigger the installation of the main package also in a fully detached manner by double-forking, then waiting for the grandparent to finish (i.e., the installer script)](https://github.com/storeman-developers/harbour-storeman-installer/blob/2.0.45/bin/harbour-storeman-installer#L192), because the main package automatically triggers the removal of the "installer" package (including its "installer" script) by a `Conflicts:` dependency on it.  This way the main package can be kept free of any special measures WRT the two stepped installation procedure (except for the single `Conflicts: <installer>` statement) and hence also can be manually and directly installed and removed after manually enabling the correct repository or downloading a suitable rpm package.

### General information about various aspects of double-forking / "daemonize"
Hence I started searching the WWW for how to perform a double-fork in shell code, without finding anything really useful for UNIX shells, but really good explanations and examples in C, Python, Ruby etc.:
- https://stackoverflow.com/questions/881388/what-is-the-reason-for-performing-a-double-fork-when-creating-a-daemon<br />
  Good, fruitful discussion of this topic, but relevant information is spread over many posts.
- https://unix.stackexchange.com/questions/715248/double-fork-why<br />
  Clean C-based example, plus discussion of the need to *double* fork on System V UNIXes with no concluding result for Linux.
- https://0xjet.github.io/3OHA/2022/04/11/post.html<br />
  Very nice and concise "low-level, abstract description" (no conundrum, really well done) of double forking.
- https://subscription.packtpub.com/book/networking-and-servers/9781784396879/11/ch11lvl1sec73/double-fork-and-setsid<br />
  This one comes close (the only shell-oriented post worth reading I found), but does only go half the way; unfortunately I found it after having determined that using `setsid` is crucial and looked for application examples.
- https://gist.github.com/mynameisrufus/1372491#file-simple_daemon-rb-L2<br />
  Another concise write-up, with example in Ruby.
- https://news.ycombinator.com/item?id=8355376<br />
  This discussion confirmed my belief at that point, that (double-)forking is the only way to go.

I wonder, why I have not found any proper and complete example for shell code, because I believe that people must have written UNIX daemons in shell code and also started them this way (e.g., per classic sysv-init), but maybe this was done in the 70s, 80s and 90s when no forums as Stackexchange, Stackoverflow or GitHub-gists etc. existed.<br />
So I ended up researching, implementing, testing and documenting this for myself and the world.
<br />

HTH
