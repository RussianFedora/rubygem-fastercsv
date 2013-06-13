%{!?ruby_sitelib:	%global ruby_sitelib	%(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")}
%{!?ruby_abiver:	%global ruby_abiver	%((echo "1.8"; ruby -rrbconfig -e "puts Config::CONFIG['ruby_version']" 2>/dev/null) | tail -1)}

%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname fastercsv
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}

Summary:	Faster, smaller and cleaner replacement to standard CSV library
Name:		rubygem-%{gemname}
Version:	1.5.5
Release:	2%{?dist}
License:	GPLv2 or Ruby
Group:		Development/Languages
URL:        http://%{gemname}.rubyforge.org/
Source0:    http://rubygems.org/downloads/%{gemname}-%{version}.gem
Requires:	ruby(abi) = %{ruby_abiver}, rubygems
Provides:	rubygem(%{gemname}) = %{version}
BuildRequires:	rubygems
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
FasterCSV is intended as a complete replacement to the CSV standard library.
It is significantly faster and smaller while still being pure Ruby code. It
also strives for a better interface.

%prep

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{gemdir}
gem install --local --install-dir $RPM_BUILD_ROOT%{gemdir} --force --rdoc %{SOURCE0}

# Find files with a shebang that do not have executable permissions
for file in $(find $RPM_BUILD_ROOT%{geminstdir} -type f ! -perm /a+x -name "*.rb"); do
  if [ ! -z "`head -n 1 $file | grep \"^#!/\"`" ]; then
    sed -e 's@/usr/local/bin/ruby@%{_bindir}/ruby@g' -i $file
    chmod -v 755 $file
  fi
done

%check
ruby -I $RPM_BUILD_ROOT%{geminstdir}/lib:$RPM_BUILD_ROOT%{geminstdir}/test $RPM_BUILD_ROOT%{geminstdir}/test/ts_all.rb

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc %{gemdir}/doc/%{gemname}-%{version}
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%dir %{gemdir}/gems/%{gemname}-%{version}/
%doc %{geminstdir}/AUTHORS
%doc %{geminstdir}/CHANGELOG
%doc %{geminstdir}/COPYING
%doc %{geminstdir}/INSTALL
%doc %{geminstdir}/LICENSE
%doc %{geminstdir}/README
%doc %{geminstdir}/TODO
%{geminstdir}/Rakefile
%{geminstdir}/examples/
%{geminstdir}/lib/
#_mx %{geminstdir}/setup.rb
%{geminstdir}/test/

%changelog
* Tue Jun 4 2013 Sergey Mihailov <sergey.mihailov@gpm.int> - 1.5.5-1
- Rebuilt for new version

* Sat Oct 08 2011 Robert Scheck <robert@fedoraproject.org> 1.5.4-1
- Upgrade to 1.5.4

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Mar 28 2010 Robert Scheck <robert@fedoraproject.org> 1.5.1-1
- Upgrade to 1.5.1

* Sun Aug 09 2009 Robert Scheck <robert@fedoraproject.org> 1.5.0-2
- Added missing requirement to ruby(abi) = version (#514928 #c1)
- Switched from defines to globals, updated summary in spec file
- Corrected license tag and removed duplicates in docs (#514928)

* Fri Jul 31 2009 Robert Scheck <robert@fedoraproject.org> 1.5.0-1
- Upgrade to 1.5.0
- Initial spec file for Fedora and Red Hat Enterprise Linux
