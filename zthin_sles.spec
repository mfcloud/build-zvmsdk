# Copyright 2024 Contributors to the Open Mainframe Project.

%define name zthin

Summary: System z hardware control point (zThin)
Name: %{name}
Version: %(cat Version)
Release: 1
Source: zthin-build.tar.gz
Vendor: IBM
License: ASL 2.0
Group: System/tools
BuildRoot: %{_tmppath}/zthin
Prefix: /opt/zthin

%description
The System z hardware control point (zThin) is a set of APIs to interface with
z/VM SMAPI. It is used to manage virtual machines running Linux on
System z.

BuildRequires: libtirpc-devel

%define builddate %(date)

%prep
tar -zxvf ../SOURCES/zthin-build.tar.gz -C ../BUILD/ --strip 1

%build
make

%install
make install

mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/opt/zthin/bin
cp smcli $RPM_BUILD_ROOT/opt/zthin/bin/
chmod 755 $RPM_BUILD_ROOT/opt/zthin/bin/smcli
mkdir -p $RPM_BUILD_ROOT/usr/share/man/man1/
cp smcli.1.gz $RPM_BUILD_ROOT/usr/share/man/man1/
mkdir -p $RPM_BUILD_ROOT/var/opt/zthin
cp config/tracing.conf $RPM_BUILD_ROOT/var/opt/zthin
cp config/settings.conf $RPM_BUILD_ROOT/var/opt/zthin
mkdir -p $RPM_BUILD_ROOT/etc/ld.so.conf.d
cp config/zthin.conf $RPM_BUILD_ROOT/etc/ld.so.conf.d
chmod -R 755 zthin/bin/*
chmod -R 755 zthin/lib/*
chmod -R 755 zthin/bin/IUCV/iucvserd
chmod -R 755 zthin/bin/IUCV/iucvserd.service
cp -rf zthin/bin/* $RPM_BUILD_ROOT/opt/zthin/bin
cp zthin/lib/* $RPM_BUILD_ROOT/opt/zthin/lib
cp zthinlogs $RPM_BUILD_ROOT/var/opt/zthin
echo "zthin version: "%{version} "Built on: "%{builddate} > $RPM_BUILD_ROOT/opt/zthin/version

make clean

%post

ln -sfd %{prefix}/bin/smcli $RPM_BUILD_ROOT/usr/bin
chmod 755 $RPM_BUILD_ROOT/usr/bin/smcli

# Create log file for zThin
mkdir -p /var/log/zthin
touch /var/log/zthin/zthin.log

# syslog located in different directories in Red Hat/SUSE
ZTHIN_LOG_HEADER="# Logging for SDK zThin"
ZTHIN_LOG="/var/log/zthin/zthin.log"
echo "Configuring syslog"

# SUSE Linux Enterprise Server
if [ -e "/etc/init.d/syslog" ]; then
    # Syslog is the standard for log messages
    grep ${ZTHIN_LOG} /etc/syslog.conf > /dev/null || (echo -e "\n${ZTHIN_LOG_HEADER}\nlocal5.*        ${ZTHIN_LOG}" >> /etc/syslog.conf)
elif [ -e "/opt/ibm/cmo/version" ]; then
    grep ${ZTHIN_LOG} /etc/rsyslog.conf > /dev/null || (echo -e "\n${ZTHIN_LOG_HEADER}\nlocal5.*        ${ZTHIN_LOG}" >> /etc/rsyslog.conf)
fi
if [ -e "/etc/syslog-ng/syslog-ng.conf" ]; then
    # Syslog-ng is the replacement for syslogd
    grep ${ZTHIN_LOG} /etc/syslog-ng/syslog-ng.conf > /dev/null || (echo -e "\n${ZTHIN_LOG_HEADER}\n\
filter f_zthin  { facility(local5); };\n\
destination zthinlog { file(\"${ZTHIN_LOG}\"); };\n\
log { source(src); filter(f_zthin); destination(zthinlog); };" >> /etc/syslog-ng/syslog-ng.conf)
fi

# Copy a zthin logrotate configuration file if it does not exist
if [ ! -f "/etc/logrotate.d/zthinlogs" ]; then
    cp /var/opt/zthin/zthinlogs /etc/logrotate.d
fi

# Restart syslog
if [ -e "/etc/rc.d/init.d/rsyslog" ]; then
    /etc/rc.d/init.d/rsyslog restart
else
    service rsyslog restart
fi

/sbin/ldconfig

%preun
# Delete man page and smcli command
# rm -rf /usr/share/man/man1/smcli.1.gz

%files
# Files provided by this package
%defattr(-,root,root)
/opt/zthin/*
%doc /usr/share/man/man1/smcli.1.gz
%config(noreplace) /var/opt/zthin/tracing.conf
%config(noreplace) /var/opt/zthin/settings.conf
%config(noreplace) /var/opt/zthin/zthinlogs
%config(noreplace) /etc/ld.so.conf.d/zthin.conf
