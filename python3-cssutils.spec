#
# Conditional build:
%bcond_without	tests		# unit tests
%bcond_with	tests_net	# unit tests using network

%define		module	cssutils
%define		encutils_ver 0.9.8
Summary:	A CSS Cascading Style Sheets library for Python
Summary(pl.UTF-8):	Biblioteka CSS (Cascading Style Sheets) dla Pythona
Name:		python3-%{module}
Version:	2.11.1
Release:	1
Epoch:		1
License:	LGPL v3+
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/c/cssutils/%{module}-%{version}.tar.gz
# Source0-md5:	c8c21e635454d9ca73b21892def35f55
URL:		http://cthedot.de/cssutils/
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-build
BuildRequires:	python3-installer
%if %{with tests}
BuildRequires:	python3-jaraco.test
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python3-modules >= 1:2.5
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A Python package to parse and build CSS Cascading Style Sheets. Partly
implements the DOM Level 2 Stylesheets and DOM Level 2 CSS interfaces.

%description -l pl.UTF-8
Pakiet Pythona do analizy i tworzenia CSS (Cascading Style Sheets).
Częściowo implementuje interfejsy DOM Level 2 Stylesheets oraz DOM
Level 2 CSS.

%prep
%setup -q -n %{module}-%{version}

%if %{without tests_net}
%{__sed} -i -e 's/def test_parseUrl/def skip_parseUrl/' cssutils/tests/test_parse.py
%{__sed} -i -e 's/def test_handlers/def skip_handlers/' cssutils/tests/test_errorhandler.py
%endif

%build
%py3_build_pyproject

%if %{with tests}
%{__python3} -m zipfile -e build-3/*.whl build-3-test
# use explicit plugins list for reliable builds (delete PYTEST_PLUGINS if empty)
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS= \
%{__python3} -m pytest -o pythonpath="$PWD/build-3-test" cssutils/tests
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

for f in csscapture csscombine cssparse ; do
	%{__mv} $RPM_BUILD_ROOT%{_bindir}/$f $RPM_BUILD_ROOT%{_bindir}/${f}-3
	ln -sf ${f}-3 $RPM_BUILD_ROOT%{_bindir}/$f
done

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/cssutils/tests

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst NEWS.rst
%attr(755,root,root) %{_bindir}/csscapture
%attr(755,root,root) %{_bindir}/csscombine
%attr(755,root,root) %{_bindir}/cssparse
%attr(755,root,root) %{_bindir}/csscapture-3
%attr(755,root,root) %{_bindir}/csscombine-3
%attr(755,root,root) %{_bindir}/cssparse-3
%{py3_sitescriptdir}/cssutils
%{py3_sitescriptdir}/encutils
%{py3_sitescriptdir}/cssutils-%{version}.dist-info
