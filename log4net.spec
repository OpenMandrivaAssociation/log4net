Summary:	A .NET framework for logging
Name:		log4net
License:	ASL 2.0
Group:		Development/Other
Version:	2.0.8
Release:	1
Url:		http://logging.apache.org/log4net/
Source0:	http://mirror.reverse.net/pub/apache/logging/log4net/source/log4net-%{version}-src.zip
Source1:	log4net.pc
#Patch0:		log4net-1.2.10-no-warnaserror.patch
BuildArch:	noarch
#BuildRequires:	nant
BuildRequires:	unzip
BuildRequires:	pkgconfig(mono)

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

sed -i 's/\r//' NOTICE
sed -i 's/\r//' README.txt
sed -i 's/\r//' LICENSE
# Remove prebuilt dll files
rm -rf bin/

# Fix for mono 4
find . -name "*.sln" -print -exec sed -i 's/Format Version 10.00/Format Version 11.00/g' {} \;
find . -name "*.csproj" -print -exec sed -i 's#ToolsVersion="3.5"#ToolsVersion="4.0"#g; s#<TargetFrameworkVersion>.*</TargetFrameworkVersion>##g; s#<PropertyGroup>#<PropertyGroup><TargetFrameworkVersion>v4.5</TargetFrameworkVersion>#g' {} \;

# Use system mono.snk key
sed -i -e 's!"..\\..\\..\\log4net.snk")]!"/etc/pki/mono/mono.snk")]!' src/AssemblyInfo.cs
sed -i -e 's!|| SSCLI)!|| SSCLI || MONO)!' src/AssemblyInfo.cs

%build
# ASF recommend using nant to build log4net
xbuild /property:Configuration=Debug /property:DefineConstants=DEBUG,MONO,STRONG src/log4net.vs2010.csproj
#nant -buildfile:log4net.build -t:mono-2.0 compile-all

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

