Summary:	A .NET framework for logging
Name:		log4net
License:	ASL 2.0
Group:		Development/Other
Version:	1.2.10
Release:	15
Url:		http://logging.apache.org/log4net/
Source0:	http://archive.apache.org/dist/incubator/%{name}/%{version}/incubating-%{name}-%{version}.zip
Source1:	log4net.pc
Patch0:		log4net-1.2.10-no-warnaserror.patch
BuildArch:	noarch
BuildRequires:	nant
BuildRequires:	unzip

%description
log4net is a tool to help the programmer output log statements to a
variety of output targets. log4net is a port of the excellent log4j
framework to the .NET runtime

%package devel
Summary:	A .NET framework for logging
Group:		Development/Other
Requires:	%{name} = %{version}-%{release}

%description devel
log4net is a tool to help the programmer output log statements to a
variety of output targets. log4net is a port of the excellent log4j
framework to the .NET runtime

%prep
%setup -q
%apply_patches
sed -i 's/\r//' NOTICE.txt
sed -i 's/\r//' README.txt
sed -i 's/\r//' LICENSE.txt
# Remove prebuilt dll files
rm -rf bin/

%build
cp /etc/pki/mono/mono.snk log4net.snk
# ASF recommend using nant to build log4net
nant -buildfile:log4net.build compile-all

%install
mkdir -p %{buildroot}/%{_datadir}/pkgconfig
cp %{SOURCE1} %{buildroot}/%{_datadir}/pkgconfig
mkdir -p %{buildroot}/%{_prefix}/lib/mono/gac/
gacutil -i bin/mono/2.0/release/log4net.dll -f -package log4net -root %{buildroot}/%{_prefix}/lib

%files
%{_prefix}/lib/mono/gac/log4net
%{_prefix}/lib/mono/log4net
%doc LICENSE.txt NOTICE.txt README.txt

%files devel
%{_datadir}/pkgconfig/log4net.pc

