# marcopolo
Distributed dependency definitions and collections

## What is this nonsense?
I'm running a service, it depends on a few other services.  I know I depend
on them. Those services do not know that I depend on them, unless I've told
them. But do other services depend on me? Keeping tabs on these dependency
chains can we very tedious and burdensome.

marcopolo provides a mechanism for collecting distributed definitions that
each service provides.  The primary data source we search currently are
GitHub.  Each service just needs to provide a valid schema file in a git
repository with a .polo extension, it can just be named .polo.

## Why call it marcopolo?
There is a game played, typically in pools, where one person that is 'it'
closes their eyes while everyone else tries not to be tagged. The person
that is 'it' calls out 'marco' and the others are supposed to respond
with 'polo' if they are not under water.  Thus the name. We call marco,
and everyone that can answer 'polo' does.

## Installation

### From source
```make install```

## Configuration

### Marco config
TBD

### Polo Schema
See examples/schema/*.polo files

## Licensing
All files contained with this distribution are licenced either under the [Apache License v2.0](http://www.apache.org/licenses/LICENSE-2.0) or the [GNU General Public License v2.0](http://www.gnu.org/licenses/gpl-2.0.html). You must agree to the terms of these licenses and abide by them before viewing, utilizing, modifying, or distributing the source code contained within this distribution.

## Build Notes

### Tests
```make test```

### Manual
* Install via makefile
```sudo make install```

### Fedora/EL6+
* Generate the RPM
```make``` or ```make rpms```

