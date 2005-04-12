
%define		mod_name	dbi_pool
%define 	apxs		/usr/sbin/apxs
Summary:	mod_dbi_pool - Pool Database connections between modules and requests
Summary(pl):	mod_dbi_pool - po³±czenia bazowanowe miêdzy modu³ami i ¿±daniami
Name:		apache-mod_%{mod_name}
Version:	0.4.0
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	http://www.outoforder.cc/downloads/mod_dbi_pool/mod_%{mod_name}-%{version}.tar.bz2
# Source0-md5:	7fd42e90358b370eafdddf1f7252a65e
URL:		http://www.outoforder.cc/projects/apache/mod_dbi_pool/
BuildRequires:	%{apxs}
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	apache-devel >= 2.0.40
BuildRequires:	libdbi-devel >= 0.7.2
BuildRequires:	libtool
BuildRequires:	pkgconfig
Requires(post,preun):	%{apxs}
Requires:	apache >= 2.0.40
Requires:	libdbi >= 0.7.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)

%description
mod_dbi_pool provides database connection pooling services for other
Apache Modules. Using libdbi it allows other modules to have a dynamic
pool of database connections for many common SQL Servers, including
mSQL, MySQL, PostgreSQL, Oracle and SQLite.

%description -l pl
mod_dbi_pool dostarcza us³ugi utrzymywania puli po³±czeñ z baz± danych
dla innych modu³ów Apache'a. Poprzez u¿ycie libdbi umo¿liwia innym
modu³om posiadanie dynamicznej puli po³±czeñ z baz± danych dla wielu
popularnych serwerów SQL, w tym mSQL, MySQL, PostgreSQL, Oracle i
SQLite.

%package devel
Summary:	Header files for mod_dbi_pool API
Summary(pl):	Pliki nag³ówkowe dla API mod_dbi_pool
Group:		Development/Libraries
Requires:	apache-devel = %{version}-%{release} >= 2.0.40

%description devel
Header files for mod_dbi_pool API.

%description devel -l pl
Pliki nag³ówkowe dla API mod_dbi_pool.

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
        --with-apxs=%{apxs}
%{__make}
%{__make} -C src make_so

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_includedir}/apache}

install src/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

install include/mod_dbi_pool.h $RPM_BUILD_ROOT%{_includedir}/apache

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{apxs} -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_pkglibdir}/*.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/apache/*.h
