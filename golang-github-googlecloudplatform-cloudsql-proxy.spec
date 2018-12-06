# Run tests in check section
# Disabled, it needs Fuse and mysql
%bcond_with check

%global goipath         github.com/GoogleCloudPlatform/cloudsql-proxy
Version:                1.11

%global common_description %{expand:
The Cloud SQL Proxy allows a user with the appropriate permissions to connect 
to a Second Generation Cloud SQL database without having to deal with IP 
whitelisting or SSL certificates manually. It works by opening unix/tcp 
sockets on the local machine and proxying connections to the associated 
Cloud SQL instances when the sockets are used.}

%gometa

Name:           %{goname}
Release:        2%{?dist}
Summary:        Connect to Second Generation Cloud SQL database
License:        ASL 2.0
URL:            %{gourl}
Source0:        %{gourl}/archive/%{version}/cloudsql-proxy-%{version}.tar.gz

#https://github.com/GoogleCloudPlatform/cloudsql-proxy/commit/f479bd5cc6091261cb04bc6e87bc0ba33d29a841
Patch0:         cloudsql-proxy-1.11-fix_errorf.patch

BuildRequires: golang(bazil.org/fuse)
BuildRequires: golang(bazil.org/fuse/fs)
BuildRequires: golang(cloud.google.com/go/compute/metadata)
BuildRequires: golang(github.com/go-sql-driver/mysql)
BuildRequires: golang(github.com/lib/pq)
BuildRequires: golang(golang.org/x/crypto/ssh)
BuildRequires: golang(golang.org/x/net/context)
BuildRequires: golang(golang.org/x/oauth2/google)
BuildRequires: golang(google.golang.org/api/compute/v1)
BuildRequires: golang(google.golang.org/api/googleapi)
BuildRequires: golang(google.golang.org/api/sqladmin/v1beta4)

%description
%{common_description}


%package devel
Summary:       %{summary}
BuildArch:     noarch

%description devel
%{common_description}

This package contains library source intended for
building other packages which use import path with
%{goipath} prefix.

%prep
%autosetup %{?forgesetupargs} -p1


%build 
%gobuildroot
%gobuild -o _bin/cloud_sql_proxy %{goipath}/cmd/cloud_sql_proxy


%install
%goinstall
install -Dpm 0755 _bin/cloud_sql_proxy %{buildroot}%{_bindir}/cloud_sql_proxy


%if %{with check}
%check
%gochecks
%endif


%files
%license LICENSE
%{_bindir}/cloud_sql_proxy


%files devel -f devel.file-list
%license LICENSE
%doc README.md Kubernetes.md CONTRIBUTORS


%changelog
* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Mar 23 2018 Robert-André Mauchin <zebob.m@gmail.com> - 1.11-1
- First package for Fedora

