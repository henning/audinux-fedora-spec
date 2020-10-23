%global debug_package %{nil}

# Global variables for github repository
%global commit0 0b96ba56379eb179423e9dcbec31a08bf0326c9f
%global gittag0 master
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name:    protrekkr
Version: 1.0.0
Release: 3%{?dist}
Summary: A jack tracker
License: GPLv2+
URL:     https://github.com/falkTX/protrekkr

Source0: https://github.com/falkTX/%{name}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
Source1: protrekkr-makefile.linux

BuildRequires: gcc gcc-c++
BuildRequires: alsa-lib-devel
BuildRequires: jack-audio-connection-kit-devel
BuildRequires: SDL-devel
BuildRequires: zlib-devel
BuildRequires: tinyxml-devel

%description
A jack tracker

%prep
%autosetup -n %{name}-%{commit0}

cp %SOURCE1 makefile.linux
sed -i -e "12,14d" src/extralibs/sdl_draw/makefile.linux
sed -i -e "s/FLAGS = -O2/FLAGS = \$(CXXFLAGS)/g" src/extralibs/sdl_draw/makefile.linux

%build

%set_build_flags

cd src/extralibs/sdl_draw
%make_build -f makefile.linux
cd ../../..
	
# -Werror=format-security -Wall
export CXXFLAGS="-O2 -g -pipe -Wp,-D_FORTIFY_SOURCE=2 -Wp,-D_GLIBCXX_ASSERTIONS -fexceptions -fstack-protector-strong -grecord-gcc-switches -specs=/usr/lib/rpm/redhat/redhat-hardened-cc1 -specs=/usr/lib/rpm/redhat/redhat-annobin-cc1 -m64 -mtune=generic -fasynchronous-unwind-tables -fstack-clash-protection -fcf-protection"
%make_build -f makefile.linux

%install

install -m 755 -d %{buildroot}/%{_datadir}/applications/
cat > %{buildroot}/%{_datadir}/applications/%{name}.desktop <<EOF
[Desktop Entry]
Version=1.0
Name=protrekkr
Comment=Mod tracker
Exec=protrekkr
Icon=protrekkr
Terminal=false
Type=Application
Categories=AudioVideo;Audio;
EOF

install -m 755 -d %{buildroot}/%{_bindir}/
install -m 644 release/distrib/ptk_linux %{buildroot}%{_bindir}/%{name}

install -m 755 -d %{buildroot}/%{_datadir}/%{name}/instruments/
install -m 644 release/distrib/instruments/* %{buildroot}%{_datadir}/%{name}/instruments/
install -m 755 -d %{buildroot}/%{_datadir}/%{name}/modules/
install -m 644 release/distrib/modules/* %{buildroot}%{_datadir}/%{name}/modules/
install -m 755 -d %{buildroot}/%{_datadir}/%{name}/presets/
install -m 644 release/distrib/presets/* %{buildroot}%{_datadir}/%{name}/presets/
install -m 755 -d %{buildroot}/%{_datadir}/%{name}/reverbs/
install -m 644 release/distrib/reverbs/* %{buildroot}%{_datadir}/%{name}/reverbs/
install -m 755 -d %{buildroot}/%{_datadir}/%{name}/skins/
install -m 644 release/distrib/skins/* %{buildroot}%{_datadir}/%{name}/skins/

install -m 755 -d %{buildroot}/%{_datadir}/icons/hicolor/32x32/apps/
install -m 644 protrekkr.jpg %{buildroot}/%{_datadir}/icons/hicolor/32x32/apps/%{name}.jpg

%files
%doc README
%license release/distrib/license.txt
%{_bindir}/*
%{_datadir}/*

%changelog
* Fri Oct 23 2020 Yann Collette <ycollette.nospam@free.fr> - 1.0.0-3
- fix debug build

* Mon Aug 31 2020 Yann Collette <ycollette.nospam@free.fr> - 1.0.0-2
- update to master - remove internal zlib dependency + cleanup

* Mon Oct 15 2018 Yann Collette <ycollette.nospam@free.fr> - 1.0.0-1
- update for Fedora 29

* Sat Jun 06 2015 Yann Collette <ycollette.nospam@free.fr> - 1.0.0-1
- Initial build
