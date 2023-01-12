# Double-fork ("daemonize") in shell code

#### Minimal form
`(umask 0022; cd /; setsid --fork sh -c '(<commmand-list>)') > /dev/null 2>&1 < /dev/null`

#### Ususally one wants to terminate the caller or wait for it to finish

##### Terminating the caller
`(umask 0022; cd /; setsid --fork sh -c '(kill $1; <commmand-list>)' <choose-a-process-name> $$) > /dev/null 2>&1 < /dev/null`

##### Waiting for the caller to finish; waits endlessly, if it does not!
`(umask 0022; cd /; setsid --fork sh -c '(while ps -eo pid | fgrep $1; do sleep 1; done; <commmand-list>)' <choose-a-process-name> $$) > /dev/null 2>&1 < /dev/null`

##### Waiting for the caller to finish with timeout, then terminating it
`(umask 0022; cd /; setsid --fork sh -c '(i=0; while [ $i != $2 ] && ps -eo pid | fgrep $1; do sleep 1; $(($i+1)); done; [ $i = $2 ] && echo "Timed out after $i seconds, killing grandparent now!" > logfile.txt; kill $1; <commmand-list>)' <choose-a-process-name> $$ <timeout-in-seconds>) > /dev/null 2>&1 < /dev/null`

#### "Generic form"
`(umask 0022; cd /; setsid --fork sh -c '(<command-list-to-execute [$1] [$2] [<…>] [individual-redirections-for-a-command]>)' [<arbitrary-name-for-$0-of-sh-c> [<parameter1-for-$1-"inside"-sh-c>] [<parameter2-for-$2-"inside"-sh-c>] [<…>]] [global-redirections-for-the-whole-command-list]) > /dev/null 2>&1 < /dev/null`

##### Minimalistic form; inerits umask, PWD and and file descriptors from caller
`setsid --fork sh -c '(<commmand-list>)'`

## Variations
- One can set umask and PWD (via `cd`) as it fits best: The exemplary values in the "generic form" are just often used ones; I usually set the umask more restrictively.<br />
  Mind that the directory to change to must exist (you do not want a `cd` at this point to fail), hence `/` is a safe value, as e.g., `/tmp` is not available early in the boot-phase (not relevant for actions triggered by a regular user).
- One sure can redirect from or to anywhere else than `/dev/null` or redirect StdIN and StdERR differently.<br />
  Consider where you want the output in error cases to go (both, StdOUT and StdERR) to be visible for debugging, too.
- If one only calls an own shell-script `sh -c '(<myscript>)'`, one could consider to pull checking / setting the umask and PWD early inside that script and also take care of input- and output-redirections there; do not, because if the initial values are dynamic (i.e., variable, hence unknown at the time the code is written) or may become invalid after the double-fork (e.g., the caller subsequently deletes the directory, which was PWD at call time) you shall set them as early as possible.  See also [the first points of the section "Notes"](#notes).
- With a POSIX-compliant shell, one can close any file descriptor with "&-" (e.g., for StdIN `<&-`, for StdOUT `>&-` and for StdERR `2>&-`), instead of redirecting it from or to `/dev/null`.<br />
  Also note that when closing StdOUT or StdERR, anything writing to a closed file descriptor will (/ might / should / must?  POSIX might tell.) fail, just as reading from a closed StdIN, in contrast to redirections from or to `/dev/null`.  This is fine if one ensures that the commands executed do not use any closed file descriptors, e.g., by redirecting them individually for single commands or commands grouped by `{ <command-list> ; }`.

## Notes
- It is strongly recommended to explicitly set umask, PWD, StdIN, StdOUT and StdERR to known good values (or ensure that they are already sane) at the top level, because they are part of the environment, as depicted in the "generic form" above.
- The environment of a caller is always copied stepwise further down the call chain and can be altered at each step; additionally some shells (e.g., busybox's ash) also copy their regular variables (the ones not exported to the environment) down to sub-shells opened with `(…)`, but this is implementation dependent, hence nothing to rely on.<br />
  Thus one can use environment variables to pass values down the call chain, though this is not elegant and clutters the environment, hence …
- The best way to carry parameters across this sequence down the call chain are positional parameters, as described in the man-page of the shell of your choice for the option `-c` and depicted in [the examples above](#double-fork-daemonize-in-shell-code).
- The innermost sub-shell call (i.e., the one "inside" the `sh -c '…'`) is only deemed necessary on System V descendent UNIXes, in order to execute the \<command-list\> in a shell, which is not a session leader (see section "[Background](background)" below).  Hence on BSD-UNIXes one may omit the innermost `(…)` and use `… setsid --fork sh -c '<cmd-list> [<individual-redirs>]' [[arg0] [<arg1>] [<arg2>]] [<global-redirs>]; …` (or for a single command: `… setsid --fork <command> [<arg1>] [<arg2>] [<redirs>]; …`) instead.  Well, Linux is a System V UNIX by design, but all code is newly and independently written, in contrast to, e.g., HP-UX, IRIX, Sinix etc. (Solaris 2?), which contain code from the original System V Release 4 ("SVR4").  I have not researched much, which property / flaw of a "System V descendent UNIX" this addresses and how real the dangers are, because once the scheme of double-forking in shell code is understood, it is easy to ensure not to be a session leader by opening a sub-shell via `(…)`.
- For terminating a (sub-)shell via SIGTERM, this shell must not be an interactive shell (POSIX requires interactive shell instances to ignore a SIGTERM: Open a shell, type `kill $$`, see that nothing happens, then `kill -HUP $$` to close it).<br />
  Thus for experimenting / testing in an interactive shell, one might wrap the whole statement (e.g., in the form of one of the examples above) in a(nother) `sh -c '…' &` (i.e., detaching it via `&`) to mimic an indepentently running shell which executes your test and target this shell instance with a `kill $!` when your experiment does not terminate on its own.
- The caller of the ["Terminating the caller" example](#terminating-the-caller) is terminated immediately after calling it.  There are some other ways to ensure that execution of the original caller ends, e.g., see [the subsequent examples above](#waiting-for-the-caller-to-finish-waits-endlessly-if-it-does-not), plus "[Larger variations](#larger-variations)", below.
- The statement must be started detached (`setsid` does that implicitly, if *not* using the option `-w`: Thus no `&` shall be appended), otherwise the caller would be stopped during the execution of the statement, hence the caller would not be able to receive and handle a SIGTERM sent to it by `kill`.
- While explicitly specifying to run the \<command-list\> in a sub-shell (by `(…)`) inside the `sh -c '…'` may be superfluous in some special cases, do not omit it: Even though IMHO all shells start a single detached command (i.e., `<cmd> [<args>] [<redirs>] &`) automatically in a sub-shell, many execute all external commands in a sub-shell etc., there might be cases in which this assumption will fall short.<br />
  Plus, expressing the execution in a sub-shell explicitly does no harm, improves readability (one does not have to know / think about the specific shell's automatisms) and enhances portability (some of this behaviour depends on the implementation).
- Double-forking / daemonising (with or without the "anti-session-leader extra-fork" for SysV-UNIXes) is impossible to achieve via `nohup` or `disown` AFAICS (e.g., trying forms as `umask 0123; cd /tmp; nohup <command> [<args>] [<redirs>] &` or `umask 7777; cd /; (<command-list>) [<global-redirs>] & disown [-h] [$!]`), because with both forms the callee will stay in the same session as the caller, with the sessions's TTY being assigned to the callee.
- If you want to check, if the process hierarchy looks as it should (see section "[Background](#background)" below), the tree-view of GNU-`ps` (option `--forest`) or `pstree` are quite useful to see the hierarchical aspects much easier, but obscure other important aspects to observe: the SessionID and TTY.<br />
  Observing the dynamics of these actions can be best achieved by instrumenting the calling and called script with `ps -o stat,tty,user,group,pgid,sid,ppid,pid,comm,args` (field names from busybox's `ps`, other `ps`-implementations may call the SessionID-field `ssid`) at appropiate locations, plus some, but not too tight filtering (e.g., `ps -eo … | grep …` etc.), and output redirection to a file (e.g., `>> mylog.txt`).  See [this branch for an example](https://github.com/storeman-developers/harbour-storeman-installer/tree/2.0.44), the minimalistic `ps` call options are used in order to work with busybox's `ps` implementation (which is not fully POSIX compliant).

## Larger variations
- Because one usually starts the whole double-fork to the innermost \<command-list\> from a shell (respectively, a script interpreted by one), one may omit the outer sub-shell call via `(…)` (as depicted in the "[minimalistic form](minimalistic-form)", above) and use the shell from which the double fork is called to set umask and PWD there; the outer sub-shell call was solely employed for not altering the callers environment.
  If the caller finishes after the double-fork, this is a logical thing to do, e.g.:<br />
  `…`<br />
  `umask 7113`<br />
  `[ "$PWD" = /tmp ] || cd /tmp  # Set PWD to /tmp, if not already`<br />
  `setsid --fork sh -c '(while ps -eo pid | fgrep $1; do sleep 1; done; <command-list [$2] [redirs-for-a-cmd]>) [redirs-for-then-cmd-list]' <name-for-$0> $$ <param2-for-$2> > /dev/null 2>&1 < /dev/null`<br />
  `[ $? = 0 ] && echo "Successfully double-forked."`<br />
  `exit 0`<br />
  Alternatively one may save some settings and then alter them before the `setsid` call, to ultimately perform the call and restore the old values afterwards, e.g.:<br />
  `…`<br />
  `curmask=$(umask)`<br />
  `umask 7137`<br />
  `pushd /  # Set PWD to root directory`<br />
  `setsid --fork sh -c '(while ps -eo pid | fgrep $1; do sleep 1; done; <command-list [$2] [redirs-for-a-cmd]>) [redirs-for-then-cmd-list]' <name-for-$0> $$ <param2-for-$2> > /dev/null 2>&1 < /dev/null`<br />
  `umask $curmask`<br />
  `popd`<br />
  `…`<br />
  A "real-life example" [can be seen here](https://github.com/storeman-developers/harbour-storeman-installer/blob/2.1.3/rpm/harbour-storeman-installer.spec#L116-L124).
- Because a long \<command-list\> "inside" the `setsid --fork sh -c '…'` is not nice to handle and maintain, one can simply put the \<command-list\> in a shell script (which might consume positional parameters) and call that via `setsid --fork sh -c '(myscript $1 $2 …)' <name-for-$0> $$ <param2-for-$2> > /dev/null 2>&1 < /dev/null`<br />
  Then `myscript` might perform the necessary actions (*except* for setting the environment, which shall be performed as early as possible: umask, PWD, redirections), e.g. (continuing to use the example introduced one bullet point above):
  ```
  #!/bin/sh
  while ps -eo pid | fgrep $1
  do sleep 1
  done
  umask 0022
  <cmd-list [$2]>
  …
  ```
  A "real-life example" [can be seen here](https://github.com/storeman-developers/harbour-storeman-installer/blob/2.1.3/bin/harbour-storeman-installer#L69-L87).

## Motivation

#### My issue: Trigger installing an RPM from a scriptlet of another one
I had to trigger the installation of an RPM package from within an spec file scriptlet of an "installer" RPM package, for which the `%posttrans` scriptlet is the natural place, as it is run last.  Side note: In general this should not be necessary, my initial reaction was "this is conceptually wrong and shall be handled by proper dependency definitions", but it turned out to be a special case with restrictions which do create a necessity for this; other workarounds would be much harder to deploy for an average user.  Here, the "installer" package has to enable an appropriate, dynamically determined repository (dependent on CPU-architecture, installed OS release etc.) in order to access the correct main package; unless this repository is enabled (i.e., as long the installation of the "installer" package has not finished), resolving dependencies for a main package cannot be performed, because the (/ any) specific main package is not yet accessible.

I know that other people have solved this by utilising `cron` or `systemd`, but after having successfully [implemented this via an indirection by a systemd unit](https://github.com/storeman-developers/harbour-storeman-installer/tree/2.0.31/), I realised:
- The indirection via `cron` or `systemd` achieves that the started process is fully detached from the caller: I.e., that the caller is not an ancestor (parent, grandparent etc.) of the callee, plus that it is run within a different session (see `ps`'s field `sid` for the SessionID) and hence does not share a TTY with the caller, any longer.
- One does not want any time-based waiting, because no one can tell how long the initial "installer" package installation will take on a non-deterministic software stack (i.e., not a real-time system); imagine a machine is heavily swapping and hence (almost) grinding to a halt.  Thus timer units or cron jobs are not suitable to implement this robustly.
- Consequently one has to transmit the PID of the `%posttrans` scriptlet interpreter (usually `bash`) to the fully detached process, when it is instanciated, so it can wait for the `%posttrans` interpreter to finish execution of the scriptlet.  Systemd allows for a single parameter to be transmitted to "instanciated units", but the wait function (a `while` or `until` loop) has to be implemented in an external script called by an `ExecStartPre=` statement (or pack the whole wait function awkwardly in an `sh -c '…'`), because systemd does not allow for loops or any other kind of programme flow control.
- That was the moment I realised that a single, own shell script is more elegant and provides one with many more degrees of freedom than being limited to systemd's unit syntax.  The only open design question was then how to become fully detached from the caller.  I remembered the concept of double-forking / "daemonizing" for UNIX daemons, which were once usually written in C, to fully detach a process from its caller.
- The final twist for a robust implementation was [to trigger the installation of the main package *also* in a fully detached manner by double-forking, then waiting for the grandparent to finish (i.e., the installer script)](https://github.com/storeman-developers/harbour-storeman-installer/blob/2.1.3/bin/harbour-storeman-installer#L207-L223), because the main package automatically triggers the removal of the "installer" package (including its "installer" script) by a `Conflicts:` dependency on it.  This way the main package can be kept free of any special measures WRT the two stepped installation procedure (except for the single `Conflicts: <installer>` statement) and thus can still be directly installed after manually enabling the correct repository or downloading a suitable RPM package.

#### General information about various aspects of double forking / daemonising
Hence I started searching the WWW for how to perform a double fork / daemonise in shell code, without finding anything really useful for UNIX shells, but really good explanations and examples in C, Python, Ruby etc.:
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
So I ended up researching, implementing, testing and documenting this for myself and everybody else.
<br />

HTH
