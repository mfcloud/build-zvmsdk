%define name python-zvm-sdk
%define _buildnum %(date +%Y%m%d%H%M)

Summary: IBM z/VM cloud connector
Name: %{name}
Version: 1.5.0
Release: 11.ibm.%{_buildnum}%{?dist}
Source: python-zvm-sdk.tar.gz
Vendor: IBM
License: ASL 2.0
BuildArch: noarch
Group: System/tools
Autoreq: no
Requires: python >= 2.7, python-netaddr >= 0.7.5, python2-PyJWT >= 1.0.1, python2-requests >= 2.6.0, python-routes >= 2.2, python-webob >= 1.2.3, python2-jsonschema >= 2.3.0, python-six >= 1.9.0, zthin >= 3.1.0, python-jinja2 >= 2.10, PyYAML>=3.10
BuildRoot: %{_tmppath}/python-zvm-sdk
Prefix: /opt/python-zvm-sdk

%description
The System z/VM cloud connector is a set of APIs to be used
by external API consumer.

%prep
tar -zxvf ../SOURCES/python-zvm-sdk.tar.gz -C ../BUILD/ --strip 1

%build
python setup.py build

%install
python setup.py install --single-version-externally-managed -O1 --root=%{buildroot} --record=INSTALLED_FILES

mkdir -p %{buildroot}/var/lib/zvmsdk
mkdir -p %{buildroot}/etc/zvmsdk
mkdir -p %{buildroot}/var/log/zvmsdk
mkdir -p %{buildroot}/var/opt/zvmsdk
cp zvmsdklogs %{buildroot}/var/opt/zvmsdk
cp tools/share/zvmguestconfigure  %{buildroot}/var/lib/zvmsdk/
cp tools/share/zvmguestconfigure.service %{buildroot}/var/lib/zvmsdk/

%clean
rm -rf %{buildroot}

%files -f INSTALLED_FILES
%defattr(-,root,root)
/var/lib/zvmsdk/zvmguestconfigure
/var/lib/zvmsdk/zvmguestconfigure.service
%dir %attr(0755, zvmsdk, zvmsdk) /etc/zvmsdk
%dir %attr(0755, zvmsdk, zvmsdk) /var/log/zvmsdk
%dir %attr(0755, zvmsdk, zvmsdk) /var/opt/zvmsdk
%dir %attr(0755, zvmsdk, zvmsdk) /var/lib/zvmsdk

%config(noreplace) /var/opt/zvmsdk/zvmsdklogs

%pre
/usr/bin/getent passwd zvmsdk >/dev/null || /usr/sbin/useradd -r -d /var/lib/zvmsdk -m -U zvmsdk -s /bin/bash 2>/dev/null 1>&2

%post
chown zvmsdk /var/lib/zvmsdk/setupDisk
chgrp zvmsdk /var/lib/zvmsdk/setupDisk
chown zvmsdk /etc/zvmsdk/*
chgrp zvmsdk /etc/zvmsdk/*

if [ ! -f "/etc/logrotate.d/zvmsdklogs" ]; then
    cp /var/opt/zvmsdk/zvmsdklogs /etc/logrotate.d
fi

# call zvmsdk-gentoken to create init token
zvmsdk-gentoken

chown zvmsdk /etc/zvmsdk/token.dat
chgrp zvmsdk /etc/zvmsdk/token.dat
chmod 0600 /etc/zvmsdk/token.dat


%postun
/usr/bin/getent passwd zvmsdk >/dev/null && userdel zvmsdk 2>/dev/null 1>&2

rm -fr /etc/logrotate.d/zvmsdklogs
