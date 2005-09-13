
%define		mod_name	dbi_pool
%define 	apxs		/usr/sbin/apxs
Summary:	mod_dbi_pool - Pool Database connections between modules and requests
Summary(pl):	mod_dbi_pool - po��czenia bazowanowe mi�dzy modu�ami i ��daniami
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
BuildRequires:	sed
Requires:	apache >= 2.0.40
Requires:	libdbi >= 0.7.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)
%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)

%description
mod_dbi_pool provides database connection pooling services for other
Apache Modules. Using libdbi it allows other modules to have a dynamic
pool of database connections for many common SQL Servers, including
mSQL, MySQL, PostgreSQL, Oracle and SQLite.

%description -l pl
mod_dbi_pool dostarcza us�ugi utrzymywania puli po��cze� z baz� danych
dla innych modu��w Apache'a. Poprzez u�ycie libdbi umo�liwia innym
modu�om posiadanie dynamicznej puli po��cze� z baz� danych dla wielu
popularnych serwer�w SQL, w tym mSQL, MySQL, PostgreSQL, Oracle i
SQLite.

%package devel
Summary:	Header files for mod_dbi_pool API
Summary(pl):	Pliki nag��wkowe dla API mod_dbi_pool
Group:		Development/Libraries
Requires:	apache-devel >= 2.0.40

%description devel
Header files for mod_dbi_pool API.

%description devel -l pl
Pliki nag��wkowe dla API mod_dbi_pool.

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}

sed -i -e 's,test_paths="/usr/lib /usr/local/lib",test_paths="/usr/%{_lib} /usr/lib",g' configure

%configure \
        --with-apxs=%{apxs}
%{__make}
%{__make} -C src make_so

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_includedir}/apache,%{_sysconfdir}/httpd.conf}

install src/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

install include/mod_dbi_pool.h $RPM_BUILD_ROOT%{_includedir}/apache
cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/75_%{mod_name}.conf
LoadModule %{mod_name}_module        modules/mod_%{mod_name}.so
# vim: filetype=apache ts=4 sw=4 et
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*.conf
%attr(755,root,root) %{_pkglibdir}/*.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/apache/*.h
