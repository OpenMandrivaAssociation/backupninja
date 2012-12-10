%define _enable_debug_packages %{nil}
%define debug_package          %{nil}

Summary:	Lightweight, extensible meta-backup system
Name:		backupninja
Version:	0.9.10
Release:	%mkrel 1
License:	GPLv2
Group:		Archiving/Backup
URL:		http://dev.riseup.net/backupninja/
Source0:	https://labs.riseup.net/code/projects/backupninja/files/242/%{name}-%{version}.tar.gz
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
Patch0:		automake1.12.patch

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
%patch0 -p1

%build
#autoreconf -fi
./autogen.sh
%configure2_5x \
    --libdir=%{_prefix}/lib \
    --localstatedir=/var
%make

%install
%makeinstall_std
install -d %{buildroot}%{_sysconfdir}/backup.d
install -d %{buildroot}/var/backups
install -d %{buildroot}/var/log
install -d %{buildroot}/var/lib/backupninja/reports
touch %{buildroot}/var/log/backupninja.log

%post
%create_ghostfile /var/log/backupninja.log root root 644

%files
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%config %{_sysconfdir}/cron.d/backupninja
%config %{_sysconfdir}/logrotate.d/backupninja
%config(noreplace) %{_sysconfdir}/backupninja.conf
%attr(0750,root,root) %dir %{_sysconfdir}/backup.d
%{_sbindir}/*
%{_datadir}/backupninja
%attr(0750,root,root) %dir /var/backups
%attr(0750,root,root) %dir /var/lib/backupninja
%attr(0750,root,root) %dir /var/lib/backupninja/reports
%ghost /var/log/backupninja.log
%{_mandir}/man1/*
%{_mandir}/man5/*
