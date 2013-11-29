#
# Conditional build:
%bcond_without	tests		# build without tests
%bcond_with	tests_online	# build with tests reqiuring online access

Summary:	C git library
Summary(pl.UTF-8):	Biblioteka git dla C
Name:		libgit2
Version:	0.20.0
Release:	1
License:	GPL v2 with linking exception
Group:		Libraries
Source0:	https://github.com/libgit2/libgit2/archive/v%{version}.tar.gz?/%{name}-%{version}.tar.gz
# Source0-md5:	e35f613a37e11354f34249f2faa68237
Patch0:	        %{name}-test-online.patch
Patch1:	        %{name}-no-libgit2-test.patch
URL:		http://libgit2.github.com/
BuildRequires:	cmake >= 2.6
BuildRequires:	http-parser-devel
BuildRequires:	libssh2-devel
BuildRequires:	openssl-devel
%{?with_tests:BuildRequires:	python}
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
%cmake .. \
	%{?with_tests_online:-DONLINE_TESTS=1}
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
%attr(755,root,root) %ghost %{_libdir}/libgit2.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgit2.so
%{_includedir}/git2.h
%{_includedir}/git2
%{_pkgconfigdir}/libgit2.pc
