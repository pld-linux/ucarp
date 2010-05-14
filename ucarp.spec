Summary:	Common Address Redundancy Protocol (CARP) for Unix
Summary(pl.UTF-8):	CARP (Common Address Redundancy Protocol) dla Uniksa
Name:		ucarp
Version:	1.5.1
Release:	4
License:	BSD
Group:		Applications/Networking
Source0:	ftp://ftp.ucarp.org/pub/ucarp/%{name}-%{version}.tar.gz
# Source0-md5:	391caa69fc17ffbc8a3543d8692021c9
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.config.template
URL:		http://www.ucarp.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	libpcap-devel
BuildRequires:	libtool
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
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name} $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig} $RPM_BUILD_ROOT%{_varrun}/%{name}
install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
cp -a %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
cp -a %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/config.template
install -p examples/linux/vip-down.sh $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
install -p examples/linux/vip-up.sh $RPM_BUILD_ROOT%{_sysconfdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add ucarp
%service ucarp restart "UCARP"

%preun
if [ "$1" = "0" ]; then
	%service ucarp stop
	/sbin/chkconfig --del ucarp
fi

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(755,root,root) %{_sbindir}/*
%{_sysconfdir}/%{name}
%{_sysconfdir}/%{name}/*
%attr(750,root,root) %{_sysconfdir}/%{name}/vip-down.sh
%attr(750,root,root) %{_sysconfdir}/%{name}/vip-up.sh
%{_varrun}/%{name}
