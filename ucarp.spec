Summary:	Common Address Redundancy Protocol (CARP) for Unix
Summary(pl.UTF-8):	CARP (Common Address Redundancy Protocol) dla Uniksa
Name:		ucarp
Version:	1.5.2
Release:	6
License:	BSD
Group:		Applications/Networking
Source0:	ftp://ftp.ucarp.org/pub/ucarp/%{name}-%{version}.tar.gz
# Source0-md5:	e3caa733316a32c09e5d3817617e9145
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.config.template
Source4:	%{name}.tmpfiles
Source5:    ucarp-service-generator
Source6:    ucarp.target
Source7:    ucarp@.service
URL:		http://www.ucarp.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-tools
BuildRequires:	libpcap-devel
BuildRequires:	libtool
BuildRequires:  rpmbuild(macros) >= 1.671
BuildRequires:  systemd-devel
Requires(post,preun):   /sbin/chkconfig
Requires(post,preun,postun):    systemd-units >= 38
Requires:   systemd-units >= 38
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
UCARP allows a couple of hosts to share common virtual IP addresses in
order to provide automatic failover. It is a portable userland
implementation of the secure and patent-free Common Address Redundancy
Protocol (CARP, OpenBSD's alternative to the VRRP).

Strong points of the CARP protocol are: very low overhead,
cryptographically signed messages, interoperability between different
operating systems and no need for any dedicated extra network link
between redundant hosts.

%description -l pl.UTF-8
UCARP pozwala kilku hostom na dzielenie wspólnych wirtualnych adresów
IP w celu automatycznego przejmowania w przypadku awarii. Jest to
przenośna implementacja w przestrzeni użytkownika bezpiecznego i
wolnego od patentów protokołu CARP (Common Address Redundancy Protocol
- alternatywy OpenBSD dla VRRP).

Silne punkty protokołu CARP to: bardzo mały narzut, kryptograficznie
podpisywanie komunikaty, współdziałanie między różnymi systemami
operacyjnymi i brak potrzeby dedykowanego dodatkowego połączenia
sieciowego między nadmiarowymi hostami.

%prep
%setup -q

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name} \
	$RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig} \
	$RPM_BUILD_ROOT%{_varrun}/%{name} \
	$RPM_BUILD_ROOT/usr/lib/tmpfiles.d \
    $RPM_BUILD_ROOT{%{systemdtmpfilesdir},%{systemdunitdir}} \
    $RPM_BUILD_ROOT/lib/systemd/system-generators

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
cp -a %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
cp -a %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/config.template
install -p examples/linux/vip-down.sh $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
install -p examples/linux/vip-up.sh $RPM_BUILD_ROOT%{_sysconfdir}/%{name}

install %{SOURCE4} $RPM_BUILD_ROOT/usr/lib/tmpfiles.d/%{name}.conf

install -p %{SOURCE5} $RPM_BUILD_ROOT/lib/systemd/system-generators/ucarp-service-generator
install -p %{SOURCE6} $RPM_BUILD_ROOT%{systemdunitdir}/ucarp.target
install -p %{SOURCE7} $RPM_BUILD_ROOT%{systemdunitdir}/ucarp@.service
ln -s /dev/null $RPM_BUILD_ROOT%{systemdunitdir}/ucarp.service

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add ucarp
%service ucarp restart "UCARP"
%systemd_post ucarp.target

%preun
if [ "$1" = "0" ]; then
	%service ucarp stop
	/sbin/chkconfig --del ucarp
fi
%systemd_preun ucarp.target

%postun
%systemd_reload

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(755,root,root) /lib/systemd/system-generators/%{name}-service-generator
%{systemdunitdir}/%{name}.service
%{systemdunitdir}/%{name}.target
%{systemdunitdir}/%{name}@.service
%attr(755,root,root) %{_sbindir}/*
%attr(770,root,root) %dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/config.template
%config(noreplace) %verify(not md5 mtime size) %attr(750,root,root) %{_sysconfdir}/%{name}/vip-down.sh
%config(noreplace) %verify(not md5 mtime size) %attr(750,root,root) %{_sysconfdir}/%{name}/vip-up.sh
/usr/lib/tmpfiles.d/%{name}.conf
%{_varrun}/%{name}
