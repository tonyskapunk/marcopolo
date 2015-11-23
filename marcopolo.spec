%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%{!?__initddir: %define __initddir /etc/rc.d/init.d}
%{!?_unitdir: %define _unitdir /usr/lib/systemd/system}

Name:           marcopolo
Version:        0.1.0
Release:        1%{?dist}
Group:          Applications/Systems
Summary:        Application agnostic tool to represent node availability.

License:        ASLv2
URL:            https://github.com/rackerlabs/marcopolo
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:  python-setuptools
Requires(pre):  shadow-utils
Requires:       python
Requires:       python-setuptools

%if 0%{?rhel} == 5 || 0%{?rhel} == 6
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(preun): initscripts
%else
Requires(post): systemd
Requires(preun): systemd
Requires(preun): systemd
BuildRequires: systemd
%endif

%description
Plight is a lightweight daemon providing a state machine to be
used for determining the active functionality of a machine. Such
as "in rotation" (enabled) or "in maintenance" (disabled).
The states are also configurable.


%prep
%setup -q -n %{name}-%{version}


%build

%pre
/usr/bin/getent group marcopolo >/dev/null || /usr/sbin/groupadd -r marcopolo
/usr/bin/getent passwd marcopolo >/dev/null || \
    /usr/sbin/useradd -r -g marcopolo -d /var/lib/marcopolo -s /sbin/nologin \
    -c "System account for marcopolo daemon" marcopolo
exit 0

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --root $RPM_BUILD_ROOT
mkdir -p %{buildroot}%{_localstatedir}/log/%{name}
mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}
mkdir -p %{buildroot}%{_initddir}
mkdir -p %{buildroot}%{_unitdir}
%if 0%{?rhel} == 5 || 0%{?rhel} == 6
    mv %{buildroot}/etc/init.d/%{service_name}.init %{buildroot}%{__initddir}/%{service_name}
    rm -rf %{buildroot}%{_unitdir}
%else
    rm -rf %{buildroot}/etc/init.d
%endif



%post
%if 0%{?rhel} == 5 || 0%{?rhel} == 6
  /sbin/chkconfig --add %{service_name}
%else
  %systemd_post %{service_name}.service
%endif
if [ $1 -eq 2 ] ; then
  if [ -f /var/tmp/node_disabled ]; then
    mv /var/tmp/node_disabled /var/lib/marcopolo/node_disabled
  fi
fi


%preun
%if 0%{?rhel} == 5 || 0%{?rhel} == 6
  if [ $1 -eq 0 ] ; then
    /sbin/service %{service_name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{service_name}
  fi
%else
  %systemd_preun %{service_name}.service
%endif

%postun
if [ "$1" -ge "1" ] ; then
%if 0%{?rhel} == 5 || 0%{?rhel} == 6
  /sbin/service %{service_name} condrestart >/dev/null 2>&1 || :
%else
  %systemd_postun_with_restart %{service_name}.service
%endif
fi

%files
%doc README.md
%{python_sitelib}/%{name}
%{python_sitelib}/%{name}*.egg-info
%config(noreplace) %attr(0644,marcopolo,marcopolo) %{_sysconfdir}/%{name}.conf
%attr(0755,-,-) %{_bindir}/%{name}
%dir %attr(0755,marcopolo,marcopolo) %{_localstatedir}/log/%{name}/
%ghost %dir %attr(0755,marcopolo,marcopolo) %{_localstatedir}/run/%{name}/
%dir %attr(0755,marcopolo,marcopolo) %{_localstatedir}/lib/%{name}/
%if 0%{?rhel} == 5 || 0%{?rhel} == 6
  %attr(0755,-,-) %{_initrddir}/%{service_name}
%else
  %{_unitdir}/%{service_name}.service
%endif

%changelog
* Sun Nov 22 2015 Greg Swift <greg.swift@rackspace.com> - 0.1.0-1
- Initial import
