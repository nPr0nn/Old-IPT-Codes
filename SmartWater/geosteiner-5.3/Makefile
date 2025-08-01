#***********************************************************************
#
#	$Id: Makefile.in,v 1.102 2023/04/03 16:26:02 warme Exp $
#
#	File:	Makefile.in
#	Rev:	e-7
#	Date:	04/03/2023
#
#	Copyright (c) 1993, 2023 by David M. Warme.  This work is
#	licensed under a Creative Commons Attribution-NonCommercial
#	4.0 International License.
#
#***********************************************************************
#
#	Makefile for GeoSteiner.
#
#***********************************************************************
#
#	Modification Log:
#
#	a-1:	02/20/93	warme
#		: Created.
#	b-1:	11/14/96	warme
#		: Renamed and split some files.
#		: General cleanup for release.
#	c-1:	12/20/98	warme
#		: Now using GNU autoconf.
#	c-2:	02/28/2001	warme
#		: Changes for 3.1 release.
#		: Support for GMP, new targets, new/renamed files,
#		:  updated dependencies, use explicit dependencies for
#		:  building the lp_solve subdir.
#		: Expand indirect includes in dependencies so that
#		:  we never have to "touch" any .h files.
#	d-1:	02/25/2006	warme
#		: Removed geogui from the make.  It is now a
#		:  separate package.
#	e-1:	04/14/2015	warme
#		: Changes for 5.0 release.
#		: Added automatic creation of make dependencies.
#		: Added "tar" and "doc" targets.
#		: Switch main file lists to be source files names
#		:  instead of object file names.
#	e-2:	12/12/2015	warme
#		: Added RELEASE_NOTES.
#	e-3:	09/05/2016	warme
#		: Fix libtool for OSX/Darwin.
#		: Split off fatal.[ch] and new.c from utils.c
#		:  (to avoid dragging LP solver and other unnecessary
#		:  stuff into rand_points when linking).
#		: Changes for building new rand_points program,
#		:  which is now split into several source files.
#		: Update args to rand_points program.
#		: Added costextension.h.
#		: Change notices for 5.1 release.
#	e-4:	09/05/2016	warme
#		: Add missing files to fix 'make tar'.
#	e-5:	09/24/2016	warme
#		: Remove gcc -ffloat-store option, add -Wall -Werror.
#		: Add bitmaskmacros.h, dt.h, emst.h, expand.h,
#		:  fputils.[ch], geomtypes.h, greedy.h gsttypes.h, io.h,
#		:  machine.h, mst.h, p1read.h, parms.h, point.h,
#		:  prepostlude.h, rmst.h, sll.h, utils.h.
#		: Remove general.h, rename.h.
#		: Fix building of triangle.
#	e-6:	11/18/2022	warme
#		: Add callback.[ch].
#		: Add WERROR_FLAG from configure script.
#	e-7:	04/03/2023	warme
#		: Add fputils_{cpu}.h and fputils_{cpu}_code.h.
#
#***********************************************************************
#

# Library path
LIB_PATH = ./

# Latex - only for producing the manual
LATEX = latex -interaction=batchmode 

GEOLIB_VERSION_MAJOR = 5
GEOLIB_VERSION_MINOR = 3
GEOLIB_VERSION_PATCH = 0
GEOLIB_VERSION_STRING = 5.3.0

# FIXME:
# The LEDA stuff currently only works at DIKU and it is only used when one
# writes 'make leda' which produces a small program using a LEDA interface
# to GeoSteiner (see ledamain.cc).
LEDA_DIR = /usr/local/projects/disk02/algorithm/LEDA-4.3
LEDA_CFLAGS = -I$(LEDA_DIR)/incl/
LEDA_LIBS = -L$(LEDA_DIR) -lL -lG -lP
# If LEDA-graphics are used then add: -L/usr/X11R6/lib -lW -lX11

# The subdir containing the version of lp_solve we use.
LP_SOLVE_DIR = lp_solve_2.3

# This program can work with either of two different LP solvers:
# CPLEX (a high quality commercial product) or lp_solve (public domain).
# Variables that depend upon the LP solver used.

CPLEX_HEADER_DIR = 
CPLEX_LIB_DIR = 

LP_PKG = lp_solve
LP_CFLAGS = -I$(LP_SOLVE_DIR)
LP_DEPS = $(LP_SOLVE_DIR)/lpkit.h
LP_LIBS = $(LP_SOLVE_DIR)/libLPS.a


TRIANGLE_C = 

CLIENT_LP_LIBS = 

GMP_INCLUDE_DIR = 
GMP_CFLAGS = 
GMP_LIBS = -lgmp

CTYPE_C = 

# Configure the proper C compiler and optimizer/debug options
# DEBUG_FLAGS = -g

# Installation directories:

prefix = /usr/local
exec_prefix = ${prefix}
bindir = ${exec_prefix}/bin
datadir = ${prefix}/share
includedir = ${prefix}/include
libdir = ${exec_prefix}/lib

# Make support

SHELL = /bin/sh

# Various Programs we use

CC = gcc
OPTFLAGS = -O3
WERROR_FLAG = 

# Force libtool to use C language conventions, rather than letting it
# try to guess which language we are using.
LIBTOOL = /usr/bin/libtool --tag=CC

INSTALL = /usr/bin/install -c
INSTALL_PROGRAM = $(INSTALL) -m 755
INSTALL_DATA = $(INSTALL) -m 644

# Should not need to change anything below here...

#OPTFLAGS += -DWATCH_MEMORY

dash_I_args = $(LP_CFLAGS) $(GMP_CFLAGS)

CFLAGS = $(OPTFLAGS) $(DEBUG_FLAGS) $(dash_I_args) -Wall $(WERROR_FLAG)

PROGRAMS = \
	analyze_ckpt \
	bb \
	demo1 \
	demo2 \
	demo3 \
	demo4 \
	dumpfst \
	efst \
	fst2graph \
	hgmst \
	lib_points \
	merge_ckpt \
	plotfst \
	prunefst \
	rand_points \
	rfst \
	smt \
	ufst

TARGETS = \
	geosteiner.h \
	$(PROGRAMS) \
	fpdebug.o \
	geosteiner_config \
	geosteiner_config.install \
	libgeosteiner.la

# Object file sets for each program/library...

MEMORY = memory.o

PROGRAM_SRC = \
	analyze.c \
	analyze_ckpt.c \
	bbmain.c \
	docgen.c \
	dumpfst.c \
	efstmain.c \
	fpdebug.c \
	fst2graphmain.c \
	genps.c \
	hgmstmain.c \
	memory.c \
	merge_ckpt.c \
	plotfst.c \
	prunefstmain.c \
	rfstmain.c \
	smtmain.c \
	ufstmain.c

# Source files that:
#	1. Are NOT stand-alone programs, but
#	2, Do NOT go in the library.

PROGRAM_AUX_SRC = \
	gstaes256.c \
	prng_aes256.c \
	prng_legacy.c \
	prng_new.c

LIB_SRC = \
	bb.c \
	bbsubs.c \
	bmst.c \
	bsd.c \
	btsearch.c \
	callback.c \
	channels.c \
	ckpt.c \
	constrnt.c \
	cputime.c \
	cra.c \
	cutset.c \
	cutsubs.c \
	ddsuf.c \
	dsuf.c \
	dt.c \
	efst.c \
	egmp.c \
	emptyr.c \
	emst.c \
	environment.c \
	esmt.c \
	expand.c \
	fatal.c \
	flow.c \
	fputils.c \
	fst2graph.c \
	fst.c \
	fstfuncs.c \
	greedy.c \
	heapsort.c \
	heapsortx.c \
	heapsorty.c \
	hgmst.c \
	hypergraph.c \
	incompat.c \
	io.c \
	localcut.c \
	lpinit.c \
	machine.c \
	metric.c \
	mst.c \
	nbits.c \
	new.c \
	osmt.c \
	p1read.c \
	p1write.c \
	parms.c \
	polltime.c \
	properties.c \
	prunefst.c \
	rfst.c \
	rmst.c \
	rsmt.c \
	sec2.c \
	sec_comp.c \
	sec_heur.c \
	sll.c \
	smt.c \
	solver.c \
	sortints.c \
	$(TRIANGLE_C) \
	ub.c \
	ufst.c \
	utils.c \
	weak.c

HEADER_FILES = \
	analyze.h \
	bb.h \
	bbsubs.h \
	bitmaskmacros.h \
	bmst.h \
	bsd.h \
	btsearch.h \
	callback.h \
	channels.h \
	ckpt.h \
	constrnt.h \
	costextension.h \
	cputime.h \
	cra.h \
	ctype.c \
	cutset.h \
	ddsuf.h \
	dsuf.h \
	dt.h \
	efst.h \
	efuncs.h \
	egmp.h \
	emptyr.h \
	emst.h \
	environment.h \
	errordefs.h \
	expand.h \
	fatal.h \
	flow.h \
	fpdebug.h \
	fputils.h \
	fputils_arm64.h \
	fputils_arm64_code.h \
	fputils_x86.h \
	fputils_x86_code.h \
	fstfuncs.h \
	genps.h \
	geomtypes.h \
	greedy.h \
	gstaes256.h \
	gsttypes.h \
	incompat.h \
	io.h \
	localcut.h \
	logic.h \
	lpinit.h \
	lpsolver.h \
	machine.h \
	memory.h \
	metric.h \
	mst.h \
	p1read.h \
	parmblk.h \
	parmdefs.h \
	parms.h \
	point.h \
	polltime.h \
	prepostlude.h \
	propdefs.h \
	rand_points.h \
	rfst.h \
	rmst.h \
	sec2.h \
	sec_comp.h \
	sec_heur.h \
	sll.h \
	solver.h \
	sortfuncs.h \
	steiner.h \
	triangle.h \
	triangle_rename.h \
	ub.h \
	ufst.h \
	utils.h \
	weak.h

ALL_SRC = $(PROGRAM_SRC) $(PROGRAM_AUX_SRC) $(LIB_SRC)

LIB_OBJECTS = $(LIB_SRC:.c=.lo)

ALL_OBJECTS = \
	$(LIB_OBJECTS) \
	$(LIB_OBJECTS:.lo=.o) \
	$(PROGRAM_SRC:.c=.o) \
	$(PROGRAM_AUX_SRC:.c=.o) \
	ledamain.o

ANALYZE_CKPT_OBJECTS	= analyze.o analyze_ckpt.o
BB_OBJECTS		= bbmain.o genps.o
DOCGEN_OBJECTS		= docgen.o
DUMPFST_OBJECTS		= dumpfst.o
EFST_OBJECTS		= efstmain.o
FST2GRAPH_OBJECTS	= fst2graphmain.o
HGMST_OBJECTS		= hgmstmain.o
MERGE_CKPT_OBJECTS	= merge_ckpt.o
PLOTFST_OBJECTS		= genps.o plotfst.o
PRUNEFST_OBJECTS	= prunefstmain.o
RFST_OBJECTS		= rfstmain.o
SMT_OBJECTS		= smtmain.o
UFST_OBJECTS		= ufstmain.o

#

#
# Top-level dependencies...
#

GEOLIB = $(MEMORY) -L$(LIB_PATH) -lgeosteiner $(LP_LIBS) $(GMP_LIBS) -lm

all:	$(TARGETS)

analyze_ckpt : $(ANALYZE_CKPT_OBJECTS) $(MEMORY) libgeosteiner.la
	$(CC) $(CFLAGS) -o analyze_ckpt $(ANALYZE_CKPT_OBJECTS) $(GEOLIB)

bb : $(BB_OBJECTS) $(MEMORY) libgeosteiner.la
	$(CC) $(CFLAGS) -o bb $(BB_OBJECTS) $(GEOLIB)

docgen : $(DOCGEN_OBJECTS) $(MEMORY)
	$(CC) $(CFLAGS) -o docgen $(DOCGEN_OBJECTS) $(MEMORY)

demo1 : demo1.c $(MEMORY) libgeosteiner.la
	$(CC) $(CFLAGS) -o demo1 demo1.c $(GEOLIB)

demo2 : demo2.c $(MEMORY) libgeosteiner.la
	$(CC) $(CFLAGS) -o demo2 demo2.c $(GEOLIB)

demo3 : demo3.c $(MEMORY) libgeosteiner.la
	$(CC) $(CFLAGS) -o demo3 demo3.c $(GEOLIB)

demo4 : demo4.c $(MEMORY) libgeosteiner.la
	$(CC) $(CFLAGS) -o demo4 demo4.c $(GEOLIB)

dumpfst : $(DUMPFST_OBJECTS) $(MEMORY) libgeosteiner.la
	$(CC) $(CFLAGS) -o dumpfst $(DUMPFST_OBJECTS) $(GEOLIB)

efst : $(EFST_OBJECTS) $(MEMORY) libgeosteiner.la
	$(CC) $(CFLAGS) -o efst $(EFST_OBJECTS) $(GEOLIB)

fst2graph : $(FST2GRAPH_OBJECTS) $(MEMORY) libgeosteiner.la
	$(CC) $(CFLAGS) -o fst2graph $(FST2GRAPH_OBJECTS) $(GEOLIB)

geosteiner.h : parmdefs.h errordefs.h functions.in docgen
	./docgen -h <functions.in >geosteiner.h

geosteiner_config : geosteiner_config.in Makefile
	-rm -f geosteiner_config
	sed -e 's/%GEOLIB_VERSION_STRING%/$(GEOLIB_VERSION_STRING)/' \
	    -e "s!%GEOSTEINER_CLIENT_LIBRARY_ARGS%!-L`pwd` -lgeosteiner $(CLIENT_LP_LIBS) $(GMP_LIBS) -lm!" \
	    -e "s!%GEOSTEINER_CLIENT_CFLAGS%!-I`pwd`!" \
	    <geosteiner_config.in >geosteiner_config
	chmod 755 geosteiner_config

geosteiner_config.install : geosteiner_config.in Makefile
	-rm -f geosteiner_config.install
	sed -e 's/%GEOLIB_VERSION_STRING%/$(GEOLIB_VERSION_STRING)/' \
	    -e "s!%GEOSTEINER_CLIENT_LIBRARY_ARGS%!-L$(libdir) -lgeosteiner $(CLIENT_LP_LIBS) $(GMP_LIBS) -lm!" \
	    -e "s!%GEOSTEINER_CLIENT_CFLAGS%!-I$(includedir)!" \
	    <geosteiner_config.in >geosteiner_config.install

hgmst : $(HGMST_OBJECTS) $(MEMORY) libgeosteiner.la
	$(CC) $(CFLAGS) -o hgmst $(HGMST_OBJECTS) $(GEOLIB)

libgeosteiner.la : $(LIB_OBJECTS) $(LP_LIBS)
	$(LIBTOOL) --mode=link $(CC) -static -o libgeosteiner.la $(LIB_OBJECTS) -rpath $(libdir) -lm
	cp .libs/libgeosteiner.a libgeosteiner.a

# when defining the rpath the library will be shared instead of static
#	libtool $(CC) -o libgeosteiner.la $(LIB_OBJECTS) -rpath $(LIB_PATH)
#	cp .libs/libgeosteiner.a lib/
#	cp .libs/libgeosteiner.so.0.0.0 lib/

lib_points : lib_points.c steiner.h
	$(CC) $(CFLAGS) -o lib_points lib_points.c

merge_ckpt : $(MERGE_CKPT_OBJECTS) $(MEMORY) libgeosteiner.la
	$(CC) $(CFLAGS) -o merge_ckpt $(MERGE_CKPT_OBJECTS) $(GEOLIB)

plotfst : $(PLOTFST_OBJECTS) $(MEMORY) libgeosteiner.la
	$(CC) $(CFLAGS) -o plotfst $(PLOTFST_OBJECTS) $(GEOLIB)

prunefst : $(PRUNEFST_OBJECTS) $(MEMORY) libgeosteiner.la
	$(CC) $(CFLAGS) -o prunefst $(PRUNEFST_OBJECTS) $(GEOLIB)

RAND_POINTS_OBJS = \
	gstaes256.o \
	prng_aes256.o \
	prng_legacy.o \
	prng_new.o

rand_points : rand_points.c steiner.h $(RAND_POINTS_OBJS) $(MEMORY)
	$(CC) $(CFLAGS) -o rand_points rand_points.c \
		$(RAND_POINTS_OBJS) $(GEOLIB)

rfst : $(RFST_OBJECTS) $(MEMORY) libgeosteiner.la
	$(CC) $(CFLAGS) -o rfst $(RFST_OBJECTS) $(GEOLIB)

smt : $(SMT_OBJECTS) $(MEMORY) libgeosteiner.la
	$(CC) $(CFLAGS) -o smt $(SMT_OBJECTS) $(GEOLIB)

ufst : $(UFST_OBJECTS) $(MEMORY) libgeosteiner.la
	$(CC) $(CFLAGS) -o ufst $(UFST_OBJECTS) $(GEOLIB)

# Alternative interfaces
leda : ledamain.cc libgeosteiner.la
	$(CC) ledamain.cc $(CFLAGS) $(LEDA_CFLAGS) $(LEDA_LIBS) $(GEOLIB) -o leda

jgeosteiner.h : jgeosteiner.java
	javac jgeosteiner.java && \
	javah -jni jgeosteiner

jgeosteiner : jgeosteiner.c jgeosteiner.h libgeosteiner.la
	javac jgeosteiner.java && \
	$(LIBTOOL) --mode=compile gcc -c -I/usr/local/stow/include/linux/ \
		-I/usr/local/stow/stow/net/jdk-sun_1.2.2.006-i686-linux-redhat7.2/include/ \
		jgeosteiner.c && \
	$(LIBTOOL) --mode=link gcc -o libjgeosteiner.la jgeosteiner.lo \
		-lgeosteiner -Llp_solve_2.3 -lLPS \
		-rpath /tmp/ && \
	cp .libs/libjgeosteiner.so ./

# Documentation
%.eps : %.ps bbox.awk
	-rm -f $*.eps
	awk -f bbox.awk <$*.ps >$*.eps
	touch figures.stamp

%.notabs : %.c # Whoa, this got a little bit out of hand...
	expand $*.c \
	 | awk '/^\/\*.*/{last = 0;}/\*\*\// {last = 1} {if (last == 2) {print $0}} {if (last == 1) {last = 2}}' \
	 > $*.notabs

errors.tex : functions.in docgen
	./docgen -e <functions.in >errors.tex

functions.tex : functions.in docgen
	./docgen -f <functions.in >functions.tex

hgprops.tex : functions.in docgen
	./docgen -g <functions.in >hgprops.tex

FIGURES = \
	fig_ESMT.eps \
	fig_RSMT.eps \
	fig_HSMT.eps \
	fig_OSMT.eps

# For example, you can manually do "make figures; make manual.ps"
# to *force* the figures to be rebuilt.
figures: $(FIGURES)

# Note: no dependencies here!  This is somewhat bogus, but suppose you
# change functions.in and then do "make manual.ps".  Do you really want
# to wait for it to remake geosteiner.h, and recompile just about
# *everything* -- just to rebuild the $(FIGURES) before running LaTeX?
# If you really want to rebuild the figures, do "make figures" first!
figures.stamp:
	make $(FIGURES)

fig_ESMT.ps : prelude.ps rand_points efst bb
	(cat prelude.ps ; ./rand_points -g0 20 | ./efst | ./bb) > fig_ESMT.ps

fig_RSMT.ps : prelude.ps rand_points rfst bb
	(cat prelude.ps ; ./rand_points -g0 20 | ./rfst | ./bb) > fig_RSMT.ps

fig_HSMT.ps : prelude.ps rand_points ufst bb
	(cat prelude.ps ; ./rand_points -g0 20 | ./ufst -l 3 | ./bb) > fig_HSMT.ps

fig_OSMT.ps : prelude.ps rand_points ufst bb
	(cat prelude.ps ; ./rand_points -g0 20 | ./ufst -l 4 | ./bb) > fig_OSMT.ps

doc : manual.pdf

manual.pdf : manual.ps
	ps2pdf manual.ps manual.pdf

manual.ps : manual.dvi
	dvips -t letter -f manual.dvi > manual.ps

manual.dvi : manual.tex functions.tex errors.tex hgprops.tex solverprops.tex \
	     figures.stamp \
	     demo1.notabs demo2.notabs demo3.notabs demo4.notabs
	$(LATEX) manual && $(LATEX) manual && makeindex manual && $(LATEX) manual

# manual.dvi : manual.tex functions.tex errors.tex hgprops.tex solverprops.tex 
#	latex manual && makeindex manual && latex manual && latex manual

solverprops.tex : functions.in docgen
	./docgen -s <functions.in >solverprops.tex

# How to make the libLPS.a library in the lp-solve subdir...
$(LP_SOLVE_DIR)/libLPS.a : \
		$(LP_SOLVE_DIR)/Makefile.in \
		$(LP_SOLVE_DIR)/Makefile \
		$(LP_SOLVE_DIR)/lpkit.c \
		$(LP_SOLVE_DIR)/solve.c \
		$(LP_SOLVE_DIR)/debug.c \
		$(LP_SOLVE_DIR)/presolve.c \
		$(LP_SOLVE_DIR)/hash.c \
		$(LP_SOLVE_DIR)/lpbinio.c \
		$(LP_SOLVE_DIR)/lpkit.h \
		$(LP_SOLVE_DIR)/lpglob.h \
		$(LP_SOLVE_DIR)/debug.h \
		$(LP_SOLVE_DIR)/hash.h
	(cd $(LP_SOLVE_DIR); $(MAKE) libLPS.a)

clean :
	(cd $(LP_SOLVE_DIR); $(MAKE) clean)
	-rm -f $(TARGETS) $(ALL_OBJECTS) docgen libgeosteiner.*
	-rm -f $(dependency_files)
	-rm -rf .libs
	-rm -f errors.tex functions.tex hgprops.tex solverprops.tex
	-rm -f cplex.log
	-rm -f manual.aux manual.dvi manual.idx manual.ilg manual.ind \
		manual.log manual.ps manual.pdf manual.toc
	-rm -f demo1.notabs demo2.notabs demo3.notabs demo4.notabs
	-rm -f $(FIGURES) $(FIGURES:.eps=.ps) figures.stamp

distclean : clean
	-rm -f Makefile config.cache config.h config.log config.status \
		stamp-config-h
	-rm -rf autom4te.cache

#

#
# Rules for installing...
#

install : mkinstalldirs \
		$(PROGRAMS) \
		geosteiner.h \
		geosteiner_config.install \
		libgeosteiner.la \
		prelude.ps
	$(LIBTOOL) --mode=install install -c libgeosteiner.la $(libdir)/libgeosteiner.la
	for i in $(PROGRAMS); do $(INSTALL_PROGRAM) $$i $(bindir); done
	$(INSTALL_DATA) geosteiner.h $(includedir)
	$(INSTALL_PROGRAM) geosteiner_config.install $(bindir)/geosteiner_config
	$(INSTALL_DATA) prelude.ps $(datadir)

mkinstalldirs :
	for i in $(prefix) $(exec_prefix) $(bindir) $(libdir) $(includedir) $(datadir); \
	do if [ ! -d $$i ]; then mkdir $$i; fi; done

uninstall :
	(cd $(bindir) && rm -f $(PROGRAMS) geosteiner_config)
	rm -f $(includedir)/geosteiner.h
	$(LIBTOOL) --mode=uninstall uninstall $(libdir)/libgeosteiner.la
	rm -f $(datadir)/prelude.ps
#^

#
# Define list of files to distribute in the tarball.
#

files_to_distribute := \
	$(PROGRAM_SRC) \
	$(PROGRAM_AUX_SRC) \
	$(LIB_SRC) \
	$(HEADER_FILES) \
	aclocal.m4 \
	bbox.awk \
	ChangeLog \
	check_lib_syms.sh \
	config.h.in \
	configure \
	configure.ac \
	demo1.c \
	demo2.c \
	demo3.c \
	demo4.c \
	functions.in \
	geosteiner_config.in \
	INSTALL \
	install-sh \
	jgeosteiner.c \
	jgeosteiner.java \
	ledamain.cc \
	lib_points.c \
	LICENSE \
	Makefile.in \
	manual.tex \
	prelude.ps \
	rand_points.c \
	README \
	RELEASE_NOTES \
	rename.awk \
	tilted_lattice_points \
	triangle.c \
	verify.awk

files_to_distribute := $(sort $(files_to_distribute))

# These get mode 755 in the tarball instead of 644.
scripts_to_distribute := \
	bbox.awk \
	check_lib_syms.sh \
	configure \
	install-sh \
	rename.awk \
	tilted_lattice_points \
	verify.awk
#
#
# Rules for making a distribution tarball.
#

ifeq ($(GEOLIB_VERSION_PATCH),0)
 tardir = geosteiner-$(GEOLIB_VERSION_MAJOR).$(GEOLIB_VERSION_MINOR)
else
 tardir = geosteiner-$(GEOLIB_VERSION_MAJOR).$(GEOLIB_VERSION_MINOR).$(GEOLIB_VERSION_PATCH)
endif

toppath := $(shell pwd)
distdir := $(toppath)/$(tardir)

.PHONY : tar dist distree distree_subdirs

tar : disttree
	-rm -f $(tardir).tar $(tardir).tar.gz
	tar -cf $(tardir).tar $(tardir)
	gzip -9 $(tardir).tar
	-rm -rf $(tardir)

disttree : dist disttree_subdirs

dist: $(files_to_distribute)
	-@if test -e "$(distdir)"; then echo Removing $(distdir); rm -rf $(distdir); fi
	@echo Copying files...
	@mkdir $(distdir)
	@cp $(files_to_distribute) $(distdir)
	@for i in $(files_to_distribute); do touch -r $$i $(distdir)/$$i; done
	@(cd $(distdir); chmod 644 $(files_to_distribute))
	@(cd $(distdir); chmod 755 $(scripts_to_distribute))

disttree_subdirs :
	(cd $(LP_SOLVE_DIR); make dist distdir="$(distdir)/$(LP_SOLVE_DIR)")
#

#
# Rules and dependencies for reconfiguration...
#

configure : configure.ac aclocal.m4
	autoconf

config.h : stamp-config-h

stamp-config-h : config.h.in config.status
	./config.status

Makefile : Makefile.in config.status
	./config.status

$(LP_SOLVE_DIR)/Makefile : $(LP_SOLVE_DIR)/Makefile.in config.status
	./config.status

config.status : configure
	./config.status --recheck
#

#
# Rules for compiling source files.
#

%.lo : %.c
	$(LIBTOOL) --mode=compile $(CC) -c $(CFLAGS) $(CPPFLAGS) $< -o $@

%.lo : %.cc
	$(LIBTOOL) --mode=compile $(CC) -c $(CFLAGS) $(CPPFLAGS) $< -o $@

# Triangle needs less picky options.
triangle.lo : triangle.c
	$(LIBTOOL) --mode=compile $(CC) -c $(OPTFLAGS) $(DEBUG_FLAGS) $(CPPFLAGS) $< -o $@

#
# Rules for automatically making dependency files.
#

%.dep : %.c
	@echo Finding dependencies for $<
	@-rm -f $@
	@$(CC) -MM $(dash_I_args) $< \
		| sed -e 's/\($*\.o\)[ :]*/$*.o $*.lo $@ : /' \
		      -e 's!$(LP_SOLVE_DIR)/lpkit.h!$$(LP_DEPS)!' \
		      -e 's!$(LP_SOLVE_DIR)/[^	 ]*[	 ]*! !' \
		      -e 's![^	 ]*/cplex.h!$$(LP_DEPS)!' \
		      -e 's!$(CPLEX_HEADER_DIR)/[^	 ]*[	 ]*! !' \
		>$@

dependency_files = $(sort $(ALL_SRC:.c=.dep))

$(dependency_files) : Makefile geosteiner.h

# Include all of the dependency files (unless we are cleaning).
ifneq ($(MAKECMDGOALS),clean)
  ifneq ($(MAKECMDGOALS),distclean)
    ifneq ($(MAKECMDGOALS),tar)
      sinclude $(dependency_files)
    endif
  endif
endif
#

#
# Mark the include files as being "precious".
#

.PRECIOUS: $(HEADER_FILES)
