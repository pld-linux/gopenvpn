%define		gitcommit	b4192ebb8f6c319f0e1e2e5157c87e530a587ef5
%define		gitshort	%(c=%{gitcommit}; echo ${c:0:7})
Summary:	Simple graphical front-end for OpenVPN
Name:		gopenvpn
Version:	0.7
Release:	0.git%{gitshort}.1
License:	GPL v2
Group:		X11/Applications/Networking
Source0:	http://sourceforge.net/code-snapshots/git/g/go/gopenvpn/gopenvpn.git/gopenvpn-gopenvpn-%{gitcommit}.zip
# Source0-md5:	ac81518d8fbad3d56818941a3992868b
Source1:	%{name}.desktop
Patch0:		format-security.patch
URL:		http://gopenvpn.sourceforge.net/
BuildRequires:	gtk+2-devel
BuildRequires:	glib2-devel
BuildRequires:	libglade2-devel
BuildRequires:	libgnome-keyring-devel
BuildRequires:	polkit-devel
BuildRequires:	openvpn-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	intltool
BuildRequires:	gettext
Requires:	openvpn
Requires:	polkit
Suggests:	gedit
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
gopenvpn provides a GNOME system tray icon from which OpenVPN
connections can be started and stopped, and a dialog from which
OpenVPN's logs can be viewed. It can manage multiple simultaneous
connections, and graphically indicates when you're connected
to a VPN tunnel.

%prep
%setup -q -n %{name}-%{name}-%{gitcommit}
%patch -P0 -p1

%build
%{__gettextize}
%{__sed} -i -e 's|\(AC_CONFIG_FILES.*\) po/Makefile.in|\1|' configure.ac
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-openvpn=/usr/sbin/openvpn \
	--with-gedit=/usr/bin/gedit \
	--with-pkexec=/usr/bin/pkexec
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_desktopdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%attr(755,root,root) %{_bindir}/%{name}*
%{_datadir}/%{name}
%{_datadir}/polkit-1/actions/net.openvpn.gui.gopenvpn.policy
%{_desktopdir}/%{name}.desktop
