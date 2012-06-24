Summary:	Common Address Redundancy Protocol (CARP) for Unix
Summary(pl):	CARP (Common Address Redundancy Protocol) dla Uniksa
Name:		ucarp
Version:	1.1
Release:	0.1
License:	BSD
Group:		Applications/Networking
Source0:	ftp://ftp.ucarp.org/pub/ucarp/%{name}-%{version}.tar.gz
# Source0-md5:	59122fd8efd49ac18c5da60e08e93493
URL:		http://www.ucarp.org/
BuildRequires:	autoconf
BuildRequires:	automake
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

%description -l pl
UCARP pozwala kilku hostom na dzielenie wsp�lnych wirtualnych adres�w
IP w celu automatycznego przejmowania w przypadku awarii. Jest to
przeno�na implementacja w przestrzeni u�ytkownika bezpiecznego i
wolnego od patent�w protoko�u CARP (Common Address Redundancy Protocol
- alternatywy OpenBSD dla VRRP).

Silne punkty protoko�u CARP to: bardzo ma�y narzut, kryptograficznie
podpisywanie komunikaty, wsp�dzia�anie mi�dzy r�nymi systemami
operacyjnymi i brak potrzeby dedykowanego dodatkowego po��czenia
sieciowego mi�dzy nadmiarowymi hostami.

%prep
%setup -q 

%build
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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog README
%attr(755,root,root) %{_sbindir}/*
