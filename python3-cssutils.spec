#
# Conditional build:
%bcond_with	doc		# Sphinx documentation (TODO)
%bcond_without	tests		# unit tests
%bcond_with	tests_net	# unit tests using network

%define		module	cssutils
Summary:	A CSS Cascading Style Sheets library for Python
Summary(pl.UTF-8):	Biblioteka CSS (Cascading Style Sheets) dla Pythona
Name:		python3-%{module}
Version:	2.11.1
Release:	2
Epoch:		1
License:	LGPL v3+
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/cssutils/
Source0:	https://files.pythonhosted.org/packages/source/c/cssutils/%{module}-%{version}.tar.gz
# Source0-md5:	c8c21e635454d9ca73b21892def35f55
URL:		http://cthedot.de/cssutils/
BuildRequires:	python3-devel >= 1:3.8
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-setuptools >= 1:61.2
BuildRequires:	python3-setuptools_scm >= 3.4.1
%if %{with tests}
BuildRequires:	python3-cssselect
%if "%{py3_ver}" == "3.8"
BuildRequires:	python3-importlib_resources
%endif
BuildRequires:	python3-jaraco.test >= 5.1
BuildRequires:	python3-more_itertools
BuildRequires:	python3-pytest >= 6
#BuildRequires:	python3-pytest-checkdocs >= 2.4
#BuildRequires:	python3-pytest-cov
#BuildRequires:	python3-pytest-enabler >= 0.2.2
#BuildRequires:	python3-pytest-mypy
#BuildRequires:	python3-pytest-ruff
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-furo
BuildRequires:	python3-jaraco.packaging >= 9.3
BuildRequires:	python3-jaraco.tidelift >= 1.4
BuildRequires:	python3-rst.linker >= 1.9
BuildRequires:	python3-sphinx_lint
BuildRequires:	sphinx-pdg-3 >= 3.5
%endif
Requires:	python3-modules >= 1:3.8
Conflicts:	python-cssutils < 1.0.2-12
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
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest cssutils/tests
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
%doc NEWS.rst README.rst SECURITY.md
%attr(755,root,root) %{_bindir}/csscapture-3
%attr(755,root,root) %{_bindir}/csscombine-3
%attr(755,root,root) %{_bindir}/cssparse-3
%{_bindir}/csscapture
%{_bindir}/csscombine
%{_bindir}/cssparse
%{py3_sitescriptdir}/cssutils
%{py3_sitescriptdir}/encutils
%{py3_sitescriptdir}/cssutils-%{version}.dist-info
