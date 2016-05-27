#
# Conditional build:
%bcond_without	kerberos5	# GSSAPI for SPNEGO auth
%bcond_without	tests		# build without tests
%bcond_without	libssh		# Link with libssh2 to enable SSH support
%bcond_without	curl		# Use cURL for HTTP
%bcond_with	tests_online	# build with tests reqiuring online access

Summary:	C Git library
Summary(pl.UTF-8):	Biblioteka Git dla C
Name:		libgit2
Version:	0.24.0
Release:	1
License:	GPL v2 with linking exception
Group:		Libraries
Source0:	https://github.com/libgit2/libgit2/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	8cabf04502d7203793b32f47ca410ae3
Patch0:	        %{name}-test-online.patch
Patch1:	        %{name}-no-libgit2-test.patch
URL:		http://libgit2.github.com/
BuildRequires:	cmake >= 2.8
%{?with_curl:BuildRequires:	curl-devel}
%{?with_kerberos5:BuildRequires:	heimdal-devel}
BuildRequires:	http-parser-devel >= 2
%{?with_libssh:BuildRequires:	libssh2-devel}
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
%{?with_tests:BuildRequires:	python}
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# Usage: cmake_with BCOND_NAME [OPTION_NAME]
%define		cmake_with() %{expand:%%{?with_%{1}:-D%{?2}%{!?2:%{1}}=BOOL:ON}%%{!?with_%{1}:-D%{?2}%{!?2:%{1}}=BOOL:OFF}}

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
%patch1 -p1

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
	%{cmake_with curl CURL} \
	%{cmake_with kerberos5 USE_GSSAPI} \
	%{cmake_with libssh USE_SSH} \
	%{cmake_with tests_online ONLINE_TESTS} \
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
%doc AUTHORS CONTRIBUTING.md COPYING README.md
%attr(755,root,root) %{_libdir}/libgit2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgit2.so.24

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgit2.so
%{_includedir}/git2.h
%{_includedir}/git2
%{_pkgconfigdir}/libgit2.pc
