#
# Conditional build:
%bcond_without	kerberos5	# GSSAPI for SPNEGO auth
%bcond_without	libssh		# SSH support via libssh2
%bcond_with	tests		# build without tests

Summary:	C Git library
Summary(pl.UTF-8):	Biblioteka Git dla C
Name:		libgit2
Version:	1.2.0
Release:	1
License:	GPL v2 with linking exception
Group:		Libraries
#Source0Download: https://github.com/libgit2/libgit2/releases
Source0:	https://github.com/libgit2/libgit2/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	72825e8dc26c7360910a9dee070b8122
Patch0:		%{name}-no-libgit2-test.patch
URL:		http://libgit2.github.com/
BuildRequires:	cmake >= 3.5.1
%{?with_kerberos5:BuildRequires:	heimdal-devel}
BuildRequires:	http-parser-devel >= 2
%{?with_libssh:BuildRequires:	libssh2-devel}
BuildRequires:	openssl-devel
BuildRequires:	pcre-devel
BuildRequires:	pkgconfig
%{?with_tests:BuildRequires:	python}
BuildRequires:	rpmbuild(macros) >= 1.742
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libgit2 is a portable, pure C implementation of the Git core methods
provided as a re-entrant linkable library with a solid API, allowing
you to write native speed custom Git applications in any language with
bindings.

%description -l pl.UTF-8
libgit2 to przenośna implementacja w czystym C głównych metod Gita,
udostępniona jako bezpieczna dla wątków biblioteka ze stałym API,
pozwalająca na pisanie własnych aplikacji dla Gita o natywnej
szybkości w dowolnym języku posiadającym odpowiednie wiązania.

%package devel
Summary:	Header files for libgit2 library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libgit2
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	http-parser-devel
Requires:	libssh2-devel
Requires:	openssl-devel
Requires:	zlib-devel

%description devel
Header files for libgit2 library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libgit2.

%prep
%setup -q
%patch0 -p1

# Don't test network
sed -i '/ADD_TEST(online/s/^/#/' tests/CMakeLists.txt

%build
install -d build
cd build
# CMakeLists.txt supports only relative LIB_INSTALL_DIR and INCLUDE_INSTALL_DIR
# (otherwise .pc file is generated incorrectly).
# Type (:PATH or :STRING) must be specified explicitly to avoid expansion
# relative to cwd.
%cmake .. \
	-DINCLUDE_INSTALL_DIR:PATH=include \
	-DLIB_INSTALL_DIR:PATH=%{_lib} \
	%{cmake_on_off tests BUILD_CLAR} \
	%{cmake_on_off kerberos5 USE_GSSAPI} \
	%{cmake_on_off libssh USE_SSH} \
	-DUSE_HTTP_PARSER=system \
	-DTHREADSAFE:BOOL=ON
%{__make}

%{?with_tests:%{__make} test ARGS="-V"}

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
%doc AUTHORS docs/contributing.md COPYING README.md
%attr(755,root,root) %{_libdir}/libgit2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgit2.so.1.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgit2.so
%{_includedir}/git2.h
%{_includedir}/git2
%{_pkgconfigdir}/libgit2.pc
