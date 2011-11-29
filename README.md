About hex2vhd
=============

The tool is able to convert an instruction stream in HEX format to a VHDL code according to a given template.

Usage
=====

    ./hex2vhd.py -i input.hex -o output.vhd -t template.vhd

The template file is a part of the original assembler and can be downloaded on http://www.xilinx.com/picoblaze/.

What can it be used for
=======================

PicoBlaze (KCPSM3) is a soft-core processor developed by Xilinx for their FPGAs. Xilinx offers an assembler compiler which runs only on Microsoft Windows. The output in VHDL format can be then directly included into the modelled hardware.

There are also some unofficial alternatives (platform independent). But some can generate only an instruction stream in HEX format. This is a job for hex2vhd tool!

PicoBlaze compiler alternatives
-------------------------------

* [pacoblaze](http://bleyer.org/pacoblaze) -- Java
* [picoasm](http://www.xs4all.nl/~marksix/picoasm.html) -- C++
* [pico](http://http://www.stud.fit.vutbr.cz/~xvikto03/gitweb/kcpsm3.git) -- C

License
=======

Copyright (C) 2011 Jan Vcelak

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
