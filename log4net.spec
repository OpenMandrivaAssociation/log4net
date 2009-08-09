#
# spec file for package log4net (Version 1.2.9)
#
# Copyright (c) 2007 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugzilla.redhat.com

Name:		log4net
BuildRequires:	mono-data-sqlite
BuildRequires:	mono-devel
BuildRequires:	unzip
BuildRequires:	nant
URL:		http://logging.apache.org/log4net/
License:	ASL 2.0
Group:		Development/Other
Version:	1.2.10
Release:	%mkrel 1
Summary:	A .NET framework for logging
Source:		http://archive.apache.org/dist/incubator/%{name}/%{version}/incubating-%{name}-%{version}.zip
Source1:	log4net.pc
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch:	noarch

%description
log4net is a tool to help the programmer output log statements to a
variety of output targets. log4net is a port of the excellent log4j
framework to the .NET runtime

%package devel
Summary:	A .NET framework for logging
Group:		Development/Other
Requires:	%{name} = %{version}
Requires:	pkgconfig

%description devel
log4net is a tool to help the programmer output log statements to a
variety of output targets. log4net is a port of the excellent log4j
framework to the .NET runtime

%prep
%setup -q
sed -i 's/\r//' NOTICE.txt
sed -i 's/\r//' README.txt
sed -i 's/\r//' LICENSE.txt
# Remove prebuilt dll files
rm -rf bin/

%build
# create a Strong Name key to allow build to run
sn -k log4net.snk
# ASF recommend using nant to build log4net
nant -buildfile:log4net.build compile-all

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_prefix}/lib//pkgconfig
cp %{S:1} %{buildroot}/%{_prefix}/lib//pkgconfig
mkdir -p %{buildroot}/%{_prefix}/lib/mono/gac/
gacutil -i bin/mono/2.0/release/log4net.dll -f -package log4net -root %{buildroot}/%{_prefix}/lib
gacutil -i bin/mono/1.0/release/log4net.dll -package log4net -root %{buildroot}/%{_prefix}/lib

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_prefix}/lib/mono/gac/log4net
%{_prefix}/lib/mono/log4net
%doc LICENSE.txt NOTICE.txt README.txt

%files devel
%defattr(-,root,root,-)
%{_prefix}/lib/pkgconfig/log4net.pc
