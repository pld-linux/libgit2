#
# Conditional build:
%bcond_without	tests		# build without tests

Summary:	C git library
Name:		libgit2
Version:	0.18.0
Release:	1
License:	GPL v2 with linking exception
Group:		Libraries
Source0:	https://github.com/libgit2/libgit2/archive/v%{version}.tar.gz?/%{name}-version.tgz
# Source0-md5:	ce6845df0dd084ef2633a69dba64929c
URL:		http://libgit2.github.com/
BuildRequires:	cmake >= 2.6
BuildRequires:	openssl-devel
%{?with_tests:BuildRequires:	python}
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libgit2 is a portable, pure C implementation of the Git core methods
provided as a re-entrant linkable library with a solid API, allowing
you to write native speed custom Git applications in any language with
bindings.

%package devel
Summary:	Header files for %{name} library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{name} library.

%prep
%setup -q

%build
install -d build
cd build
%cmake ..
%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CONTRIBUTING.md COPYING README.md
%attr(755,root,root) %{_libdir}/libgit2.so.*.*.*
%ghost %{_libdir}/libgit2.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgit2.so
%{_includedir}/git2.h
%{_includedir}/git2
%{_pkgconfigdir}/libgit2.pc
