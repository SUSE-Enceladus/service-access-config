#
# spec file for package python-serviceAccessConfig.spec
#
# Copyright (c) 2019 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:           python3-serviceAccessConfig
Version:        0.6.0
Release:        0
Summary:        Generate access controll
License:        GPL-3.0+
Group:          System/Management
Url:            https://github.com/SUSE/Enceladus
Source0:        serviceAccessConfig-%{version}.tar.bz2
# Conflict although the package was never released in OBS, or through SLES
# it was distributed to CSPs and deployed to SUSE operated infrastructure
# servers
Conflicts:      cspInfraServerAccessConfig
%{?systemd_requires}
Requires:       python3-base
Requires:       python3-docopt
Requires:       python3-requests
BuildRequires:  python3-mock
BuildRequires:  python3-pytest
BuildRequires:  python3-requests
BuildRequires:  python3-setuptools
BuildRequires:  systemd
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

Provides:       python-serviceAccessConfig = %{version}
Obsoletes:      python-serviceAccessConfig < %{version}

%description
Automatically generate access control configuration for configured services.
Supported services are Apache, HAProxy, and Nginx.

%package test
Summary:        Tests for python-serviceAccessConfig
Group:          Development/Libraries/Python
PreReq:         python3-serviceAccessConfig = %version
Requires:       python3-mock
Requires:       python3-pytest

%description test
Package provides the unit tests for python-serviceAccessConfig

%prep
%setup -q -n serviceAccessConfig-%{version}

%build
python3 setup.py build

%install
# Code
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
mkdir -p %{buildroot}%{_sbindir}
mv %{buildroot}%{_bindir}/* %{buildroot}%{_sbindir}
# Man page
install -d -m 755 %{buildroot}/%{_mandir}/man1
install -m 644 man/man1/serviceAccessConfig.1 %{buildroot}/%{_mandir}/man1
gzip %{buildroot}/%{_mandir}/man1/serviceAccessConfig.1
# Tests
mkdir -p %{buildroot}%{python_sitelib}/tests/serviceAccessConfig
cp -r tests/* %{buildroot}%{python_sitelib}/tests/serviceAccessConfig
mkdir -p %{buildroot}/%{_unitdir}
cp -r usr/lib/systemd/system/* %{buildroot}/%{_unitdir}

%check
py.test tests/unit/test_*.py

%pre
    %service_add_pre serviceAccessConfig.service

%post
    %service_add_post serviceAccessConfig.service

%preun
    %service_del_preun serviceAccessConfig.service

%postun
    %service_del_postun serviceAccessConfig.service

%files
%defattr(-,root,root,-)
%doc README.md
%license LICENSE 
%exclude %{python_sitelib}/tests/*
%{_mandir}/man*/*
%{python3_sitelib}/*
%{_sbindir}/*
%{_unitdir}/serviceAccessConfig.service

%files test
%defattr(-,root,root,-)
%{python_sitelib}/tests/*

%changelog
