%define name python-zvm-sdk

Summary: IBM z/VM cloud connector
Name: %{name}
Version: 0.3.2
Release: 1
Source: python-zvm-sdk.tar.gz
Vendor: IBM
License: ASL 2.0
BuildArch: noarch
Group: System/tools
Autoreq: no
Requires: python >= 2.7, python-netaddr, python-jwt, python-requests, python-routes, python-webob, python-jsonschema, python-six, zthin >= 3.1.0
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


%clean
rm -rf %{buildroot}

%files -f INSTALLED_FILES
%defattr(-,root,root)

%dir %attr(0755, zvmsdk, zvmsdk) /etc/zvmsdk
%dir %attr(0755, zvmsdk, zvmsdk) /var/log/zvmsdk
%dir %attr(0755, zvmsdk, zvmsdk) /var/opt/zvmsdk
%dir %attr(0755, zvmsdk, zvmsdk) /var/lib/zvmsdk

%config(noreplace) /var/opt/zvmsdk/zvmsdklogs

%pre
/usr/bin/getent passwd zvmsdk >/dev/null || /usr/sbin/useradd -r -d /var/lib/zvmsdk -m -U zvmsdk -s /sbin/nologin 2>/dev/null 1>&2

%post
chown zvmsdk /var/lib/zvmsdk/setupDisk
chgrp zvmsdk /var/lib/zvmsdk/setupDisk
chown zvmsdk /etc/zvmsdk/*
chgrp zvmsdk /etc/zvmsdk/*

if [ ! -f "/etc/logrotate.d/zvmsdklogs" ]; then
    cp /var/opt/zvmsdk/zvmsdklogs /etc/logrotate.d
fi


%postun
userdel zvmsdk 2>/dev/null 1>&2

rm -fr /etc/logrotate.d/zvmsdklogs
