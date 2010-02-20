%define _enable_debug_packages %{nil}
%define debug_package          %{nil}

Summary:	Lightweight, extensible meta-backup system
Name:		backupninja
Version:	0.9.7
Release:	%mkrel 1
License:	GPLv2
Group:		Archiving/Backup
URL:		http://dev.riseup.net/backupninja/
Source0:	http://dev.riseup.net/backupninja/download/%{name}-%{version}.tar.gz
Requires(post): rpm-helper
Requires:	cdrdao
Requires:	cdrkit
Requires:	cdrkit-genisoimage
Requires:	dialog
Requires:	dvd+rw-tools
Requires:	hwinfo
Requires:	mailx
Requires:	mdadm
Requires:	python-pylibacl
Requires:	python-xattr
Requires:	rdiff-backup
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Backupninja lets you drop simple config files in /etc/backup.d to coordinate
system backups. Backupninja is a master of many arts, including incremental
remote filesystem backup, MySQL backup, and ldap backup. By creating simple
drop-in handler scripts, backupninja can learn new skills. Backupninja is a
silent flower blossom death strike to lost data.

In addition to backing up regular files, Backupninja has handlers to ease
backing up: ldap, maildir, MySQL, PostgreSQL, svn, trac, and the output from
shell scripts.

Backupninja currently supports common backup utilities, easing their
configuration, currently supported are: rdiff-backup, duplicity, CD/DVD

%prep
%setup -q

%build
autoreconf -fis
%configure2_5x \
    --libdir=%{_prefix}/lib \
    --localstatedir=/var
%make

%install
rm -rf %{buildroot}
%makeinstall libdir=%{buildroot}%{_prefix}/lib
install -d %{buildroot}%{_sysconfdir}/backup.d
install -d %{buildroot}/var/backups
install -d %{buildroot}/var/log
install -d %{buildroot}/var/lib/backupninja/reports
touch %{buildroot}/var/log/backupninja.log

%post
%create_ghostfile /var/log/backupninja.log root root 644

%clean
rm -fr %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%config %{_sysconfdir}/cron.d/backupninja
%config %{_sysconfdir}/logrotate.d/backupninja
%config(noreplace) %{_sysconfdir}/backupninja.conf
%attr(0750,root,root) %dir %{_sysconfdir}/backup.d
%{_sbindir}/*
%{_datadir}/backupninja
%{_prefix}/lib/backupninja
%attr(0750,root,root) %dir /var/backups
%attr(0750,root,root) %dir /var/lib/backupninja
%attr(0750,root,root) %dir /var/lib/backupninja/reports
%ghost /var/log/backupninja.log
%{_mandir}/man1/*
%{_mandir}/man5/*
