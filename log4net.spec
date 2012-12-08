Name:		log4net
BuildRequires:	unzip
BuildRequires:	nant
URL:		http://logging.apache.org/log4net/
License:	ASL 2.0
Group:		Development/Other
Version:	1.2.10
Release:	%mkrel 7
Summary:	A .NET framework for logging
Source:		http://archive.apache.org/dist/incubator/%{name}/%{version}/incubating-%{name}-%{version}.zip
Source1:	log4net.pc
Patch0:		log4net-1.2.10-no-warnaserror.patch
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
%apply_patches
sed -i 's/\r//' NOTICE.txt
sed -i 's/\r//' README.txt
sed -i 's/\r//' LICENSE.txt
# Remove prebuilt dll files
rm -rf bin/

%build
%if %mdvver >= 201100
cp /etc/pki/mono/mono.snk log4net.snk
%else
sn -k log4net.snk
%endif
# ASF recommend using nant to build log4net
nant -buildfile:log4net.build compile-all

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_datadir}/pkgconfig
cp %{S:1} %{buildroot}/%{_datadir}/pkgconfig
mkdir -p %{buildroot}/%{_prefix}/lib/mono/gac/
gacutil -i bin/mono/2.0/release/log4net.dll -f -package log4net -root %{buildroot}/%{_prefix}/lib

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_prefix}/lib/mono/gac/log4net
%{_prefix}/lib/mono/log4net
%doc LICENSE.txt NOTICE.txt README.txt

%files devel
%defattr(-,root,root,-)
%{_datadir}/pkgconfig/log4net.pc


%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 1.2.10-5mdv2011.0
+ Revision: 666092
- mass rebuild

* Thu Oct 14 2010 Götz Waschk <waschk@mandriva.org> 1.2.10-4mdv2011.0
+ Revision: 585639
- sign with central key

* Thu Oct 14 2010 Götz Waschk <waschk@mandriva.org> 1.2.10-3mdv2011.0
+ Revision: 585610
- patch to ignore build warnings
- remove .NET 1.0 binary

* Sun Aug 09 2009 Frederik Himpe <fhimpe@mandriva.org> 1.2.10-2mdv2010.0
+ Revision: 412997
- Fix location of pkgconfig file

* Sun Aug 09 2009 Frederik Himpe <fhimpe@mandriva.org> 1.2.10-1mdv2010.0
+ Revision: 412964
- First package, based on Fedora's and SUSE's SPECs
- create log4net

