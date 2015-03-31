%define		php_name	php%{?php_suffix}
%define		modname		apfd
%define		status		stable
Summary:	%{modname} - parse form data
Name:		%{php_name}-pecl-%{modname}
Version:	1.0.0
Release:	1
License:	BSD, revised
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	0f2a98864b9d8ac5a5427070645059ec
URL:		http://pecl.php.net/package/apfd/
BuildRequires:	%{php_name}-devel >= 3:5.3.0
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Provides:	php(%{modname}) = %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This tiny extension lets PHP's post handler parse
`multipart/form-data` and `application/x-www-form-urlencoded` (or any
other customly registered form data handler, like "json_post") without
regard to the request's request method.

This extension does not provide any INI entries, constants, functions
or classes.

In PECL status of this extension is: %{status}.

%package devel
Summary:	Header files for apfd PECL extension
Group:		Development/Libraries
# does not require base
Requires:	php-devel >= 4:5.2.0

%description devel
Header files for apfd PECL extension.

%prep
%setup -qc
mv %{modname}-%{version}/* .

%build
phpize
%{__libtoolize}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

install -p modules/%{modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

install -D php_apfd.h $RPM_BUILD_ROOT%{_includedir}/php/ext/apfd/php_apfd.h

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so

%files devel
%defattr(644,root,root,755)
%dir %{php_includedir}/ext/apfd
%{php_includedir}/ext/apfd/php_apfd.h
