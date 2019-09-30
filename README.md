`kill-wpull-connections` is a workaround for [wpull](https://github.com/ArchiveTeam/wpull)'s bug of HTTPS connections getting stuck, slowing down or entirely stopping progress ([#407](https://github.com/ArchiveTeam/wpull/issues/407)). It works by attaching to the process and shutting down the TCP connections directly using the `shutdown` syscall. Although written for use with wpull, it can actually be used for any process.

## Usage
To kill all TCP connections except those to 127.0.0.1 of a process:

```
kill-wpull-connections -p $PID
```

As a convenience option for ArchiveBot pipeline maintainers, to kill the connections of a running ArchiveBot job:

```
kill-wpull-connections -j $JOBID
```

If you get an error of

```
gdb.error: 'shutdown' has unknown return type; cast the call to its declared return type
```

then add the `-c` option *before* `-p` or `-j`, e.g. `kill-wpull-connections -c -p $PID`.

If you're running wpull inside a Docker container without ptrace capabilities, you need to run kill-wpull-connections outside of the container (where you do have ptrace cap) but inside the container's network namespace. One way to do this is:

```
nsenter --net=$(docker inspect $CONTAINERID | jq -r .[].NetworkSettings.SandboxKey) kill-wpull-connections -p $PID
```

## Licence
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.
