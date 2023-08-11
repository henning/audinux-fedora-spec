# Tag: Jack, MIDI
# Type: Standalone
# Category: Audio, DAW

Name:    lmms-mao-weekly
Version: 1.2.99
Release: 1%{?dist}
Summary: Linux MultiMedia Studio - Weekly version
URL:     https://lmms.io

# Because dnf does not find a carla so file
AutoReqProv: no

# - lmms itself is GPLv2+
# - included third-party code
#   - libsamplerate: GPLv2+ (but we use the system one)
# - third party code used by plugins:
#   - drumsynth files: GPLv2+ or MIT
#   - for ladspa-effecs (note that we only include cmt in the binary
#     rpm (see below):
#     - caps: GPLv2
#     - cmt: GPLv2(+?)
#     - swh: GPLv2+
#     - tap: GPLv2+
#     - calf: GPLv2+ and LGPLv2+
#   - GNU UnRTF (flp_import plugin): GPLv3+
#   - Portsmf (midi_import plugin): MIT
#   - Blip_Buffer and Gb_Snd_Emu (papu plugin): LGPLv2.1+
#   - reSID (sid plugin): GPLv2+
#   - basename.c (vst_base): Copyright only
#   - embedded zynaddsubfx plugin: GPLv2+
#     - fltk (zynaddsubfx): LGPLv2+, with exceptions (but we use
#       system's fltk)
License: GPLv2+ and GPLv2 and (GPLv2+ or MIT) and GPLv3+ and MIT and LGPLv2+ and (LGPLv2+ with exceptions) and Copyright only

Vendor:       Audinux
Distribution: Audinux

# ./lmms-source.sh <tag>
# ./lmms-source.sh master

Source0: lmms.tar.gz
Source1: lmms-source.sh

BuildRequires: gcc gcc-c++
BuildRequires: cmake
BuildRequires: git
BuildRequires: perl-List-MoreUtils
BuildRequires: perl-XML-Parser
BuildRequires: jack-audio-connection-kit-devel
BuildRequires: lv2-devel
BuildRequires: suil-devel
BuildRequires: lame-devel
BuildRequires: stk-devel
BuildRequires: SDL2-devel
BuildRequires: portaudio-devel
BuildRequires: alsa-lib-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: libsamplerate-devel
BuildRequires: libsndfile-devel
BuildRequires: fftw3-devel
BuildRequires: fluidsynth-devel
BuildRequires: libvorbis-devel
BuildRequires: libogg-devel
BuildRequires: libgig-devel
BuildRequires: ladspa-devel
BuildRequires: stk-devel
BuildRequires: qt5-qtbase-devel
BuildRequires: fltk-devel
%ifarch aarch64
BuildRequires: Carla-devel
%else
BuildRequires: Carla-mao-devel
%endif
BuildRequires: bash-completion
BuildRequires: qt5-linguist
BuildRequires: fltk-fluid
BuildRequires: desktop-file-utils

%ifarch aarch64
Requires: Carla
%else
Requires: Carla-mao
%endif
Requires: stk
Requires: libgig

%global __provides_exclude_from ^%{_libdir}/lmms/.*$
%global __requires_exclude ^libvstbase\\.so.*$|^libZynAddSubFxCore\\.so.*$

%description
LMMS aims to be a free alternative to popular (but commercial and
closed- source) programs like FruityLoops/FL Studio, Cubase and Logic
allowing you to produce music with your computer. This includes
creation of loops, synthesizing and mixing sounds, arranging samples,
having fun with your MIDI-keyboard and much more...

LMMS combines the features of a tracker-/sequencer-program and those
of powerful synthesizers, samplers, effects etc. in a modern,
user-friendly and easy to use graphical user-interface.

Features

 * Song-Editor for arranging the song
 * creating beats and basslines using the Beat-/Bassline-Editor
 * easy-to-use piano-roll for editing patterns and melodies
 * instrument- and effect-plugins
 * automation-editor
 * MIDI-support

%prep
%autosetup -n lmms

%build

%cmake -DWANT_SDL:BOOL=ON \
       -DWANT_PORTAUDIO:BOOL=ON \
       -DWANT_ALSA:BOOL=ON \
       -DWANT_JACK:BOOL=ON \
       -DWANT_WEAKJACK:BOOL=ON \
       -DWANT_PULSEAUDIO:BOOL=ON \
       -DWANT_MP3LAME:BOOL=ON \
       -DWANT_OGGVORBIS:BOOL=ON \
       -DWANT_LV2:BOOL=ON \
       -DWANT_SUIL:BOOL=ON \
       -DWANT_CAPS:BOOL=ON \
       -DWANT_SF2:BOOL=ON \
       -DWANT_STK:BOOL=ON \
       -DWANT_TAP:BOOL=ON \
       -DWANT_SWH:BOOL=ON \
       -DWANT_CMT:BOOL=ON \
       -DWANT_CALF:BOOL=ON \
       -DWANT_CARLA:BOOL=ON \
       -DWANT_LIBGIG:BOOL=ON \
       -DWANT_QT5:BOOL=ON \
       -DWANT_VST:BOOL=OFF \
       -DWANT_VST_64:BOOL=ON \
       -DCMAKE_C_FLAGS="-fPIC -DPIC" \
       -DCMAKE_EXE_LINKER_FLAGS:STRING="$LDFLAGS -pie" \
       -DCMAKE_SKIP_RPATH=OFF \
       -DCMAKE_INSTALL_LIBDIR=%{_lib} \
       -DLIBEXEC_INSTALL_DIR=%{_libexecdir}

%cmake_build

%install

%cmake_install

# workaround: copy bash completion manually into install dir because it fails during cmake install
mkdir -p %{buildroot}/%{_datadir}/bash-completion/completions
cp %{_builddir}/lmms*/doc/bash-completion/lmms %{buildroot}/%{_datadir}/bash-completion/completions/lmms

desktop-file-install --vendor '' \
        --add-category=Midi \
        --add-category=Sequencer \
        --add-category=X-Jack \
        --dir %{buildroot}%{_datadir}/applications \
        %{buildroot}%{_datadir}/applications/lmms.desktop

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/lmms.desktop

%files
%doc doc/AUTHORS README.md INSTALL.txt
%license LICENSE.txt
%{_bindir}/lmms
%{_mandir}/man1/*
%{_libdir}/lmms/
%{_datadir}/lmms/
%{_datadir}/applications/lmms.desktop
%{_datadir}/icons/hicolor/*
%{_datadir}/mime/packages/lmms.xml
%{_datadir}/bash-completion/completions/lmms
%exclude %{_includedir}/lmms

%changelog
* Thu Aug 10 2023 Yann Collette <ycollette.nospam@free.fr> - 1.3.99-1
- New package.