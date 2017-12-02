%define name python-zvm-sdk

Summary: IBM z/VM cloud connector
Name: %{name}
Version: 0.3.0
Release: 1
Source: python-zvm-sdk.tar.gz
Vendor: IBM
License: ASL 2.0
BuildArch: noarch
Group: System/tools
Requires: python-netaddr, python-jwt, python-requests, python-routes, python-webob, python-jsonschema, python-six, zthin
BuildRoot: %{_tmppath}/python-zvm-sdk
Prefix: /opt/python-zvm-sdk

%description
The System z/VM cloud connector is a set of APIs to be used
by external
%define builddate %(date)

%prep
tar -zxvf ../SOURCES/python-zvm-sdk.tar.gz -C ../BUILD/ --strip 1

%build
python setup.py build

%install
python setup.py install --single-version-externally-managed -O1 --root=%{buildroot} --prefix= --record=INSTALLED_FILES

mkdir -p %{buildroot}/var/lib/zvmsdk
mkdir -p %{buildroot}/etc/zvmsdk
mkdir -p %{buildroot}/var/log/zvmsdk


%clean
rm -rf %{buildroot}

%files -f INSTALLED_FILES
%defattr(-,root,root)

%dir %attr(0755, zvmsdk, zvmsdk) /etc/zvmsdk
%dir %attr(0755, zvmsdk, zvmsdk) /var/log/zvmsdk
%dir %attr(0755, zvmsdk, zvmsdk) /var/lib/zvmsdk

%pre
/usr/bin/getent passwd zvmsdk >/dev/null || /usr/sbin/useradd -r -d /var/lib/zvmsdk -m -U zvmsdk -s /sbin/nologin
bash -c "echo \"zvmsdk ALL = (ALL) NOPASSWD:/usr/sbin/vmcp, /opt/zthin/bin/smcli, /usr/sbin/chccwdev, /usr/sbin/cio_ignore, /usr/sbin/fdasd, /usr/sbin/fdisk, /usr/sbin/vmur, /usr/bin/mount, /usr/bin/umount, /usr/sbin/mkfs, /usr/sbin/mkfs.xfs, /usr/sbin/dasdfmt, /opt/zthin/bin/unpackdiskimage, /opt/zthin/bin/creatediskimage, /opt/zthin/bin/linkdiskandbringonline, /opt/zthin/bin/offlinediskanddetach \" > /etc/sudoers.d/zvmsdk"

%postun

