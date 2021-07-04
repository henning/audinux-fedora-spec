# Tag: Jack, Sequencer
# Type: Plugin, LV2
# Category: Audio, Effect

Summary: Multi-dimensional dynamically distorted staggered multi-bandpass LV2 plugin
Name:    BAngr
Version: 1.4.0
Release: 1%{?dist}
License: GPL
URL:     https://github.com/sjaehn/BAngr/

Source0: https://github.com/sjaehn/BAngr/archive/%{version}.tar.gz#/BAngr-%{version}.tar.gz

BuildRequires: gcc gcc-c++
BuildRequires: make
BuildRequires: lv2-devel
BuildRequires: libsndfile-devel
BuildRequires: libX11-devel
BuildRequires: xcb-util-keysyms-devel
BuildRequires: cairo-devel

%description
A multi-dimensional dynamicly distorted staggered multi-bandpass LV2 plugin, for extreme soundmangling. Based on Airwindows XRegion.

Key features:
- Multi-bandpass / distortion
- Cross-fading between four instances
- Automatic or user-controlled

%prep
%autosetup -n BAngr-%{version}

%build

%make_build PREFIX=%{_prefix} LV2DIR=%{_libdir}/lv2 DESTDIR=%{buildroot} CXXFLAGS="%{build_cxxflags} -std=c++11 -fvisibility=hidden -fPIC"

%install

%make_install PREFIX=%{_prefix} LV2DIR=%{_libdir}/lv2 DESTDIR=%{buildroot} CXXFLAGS="%{build_cxxflags} -std=c++11 -fvisibility=hidden -fPIC"

%files
%doc README.md
%license LICENSE
%{_libdir}/lv2/*

%changelog
* Sun Jul 04 2021 Yann Collette <ycollette dot nospam at free.fr> 1.4.0-1
- update to 1.4.0-1

* Sun Jun 27 2021 Yann Collette <ycollette dot nospam at free.fr> 1.2.0-1
- initial release 
