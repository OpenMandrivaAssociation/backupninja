Summary:	Lightweight, extensible meta-backup system
Name:		backupninja
Version:	1.1.0
Release:	1
License:	GPLv2
Group:		Archiving/Backup
URL:		https://0xacab.org/liberate/backupninja/
Source0:	https://0xacab.org/liberate/backupninja/-/archive/backupninja-1.1.0/backupninja-backupninja-1.1.0.tar.bz2
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
%setup -qn %{name}-%{name}-%{version}

%build
autoreconf -fis
%configure \
    --libdir=%{_prefix}/lib \
    --localstatedir=/var
%make_build

%install
%make_install libdir=%{buildroot}%{_prefix}/lib
install -d %{buildroot}%{_sysconfdir}/backup.d
install -d %{buildroot}/var/backups
install -d %{buildroot}/var/log
install -d %{buildroot}/var/lib/backupninja/reports
touch %{buildroot}/var/log/backupninja.log

%post
%create_ghostfile /var/log/backupninja.log root root 644

%files
%doc AUTHORS COPYING ChangeLog NEWS TODO
%config %{_sysconfdir}/cron.d/backupninja
%config %{_sysconfdir}/logrotate.d/backupninja
%config(noreplace) %{_sysconfdir}/backupninja.conf
%attr(0750,root,root) %dir %{_sysconfdir}/backup.d
%{_sbindir}/*
%{_datadir}/backupninja
#{_prefix}/lib/backupninja
%attr(0750,root,root) %dir /var/backups
%attr(0750,root,root) %dir /var/lib/backupninja
%attr(0750,root,root) %dir /var/lib/backupninja/reports
%ghost /var/log/backupninja.log
%{_mandir}/man1/*
%{_mandir}/man5/*
