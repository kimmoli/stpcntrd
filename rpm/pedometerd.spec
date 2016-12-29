#
# pedometer daemon spec
# (C) kimmoli 2016
#
Name:       pedometerd

%{!?qtc_qmake:%define qtc_qmake %qmake}
%{!?qtc_qmake5:%define qtc_qmake5 %qmake5}
%{!?qtc_make:%define qtc_make make}
%{?qtc_builddir:%define _builddir %qtc_builddir}

Summary:    Pedometer step counter daemon
Version:    0.0.1
Release:    1
Group:      Qt/Qt
License:    LICENSE
URL:        https://github.com/kimmoli/pedometer-daemon
Source0:    %{name}-%{version}.tar.bz2
Requires:   sensorfw-qt5 > 0.8.30
Requires:   hybris-libsensorfw-qt5 > 0.8.30

BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5DBus)
BuildRequires:  pkgconfig(mlite5)
BuildRequires:  pkgconfig(sensord-qt5)
BuildRequires:  sensorfw-qt5-devel

%description
%{summary}

%prep
%setup -q -n %{name}-%{version}

%build

%qtc_qmake5 SPECVERSION=%{version}

%qtc_make %{?_smp_mflags}

%install
rm -rf %{buildroot}

%qmake5_install

%preun
# in case of complete removal, stop and disable
if [ "$1" = "0" ]; then
  systemctl-user stop pedometerd
  systemctl-user disable pedometerd
fi

%post
systemctl-user daemon-reload
systemctl-user start pedometerd
systemctl-user enable pedometerd

%pre
# In case of update, stop first
if [ "$1" = "2" ]; then
  systemctl-user stop pedometerd
  systemctl-user disable pedometerd
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}
/etc/systemd/user/
