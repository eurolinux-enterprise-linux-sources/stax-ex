Name: stax-ex
Version: 1.7.1
Release: 4%{?dist}
Summary: StAX API extensions
Group: Development/Libraries
License: CDDL or GPLv2
Url: https://stax-ex.dev.java.net

# svn export https://svn.java.net/svn/stax-ex~svn/tags/stax-ex-1.7.1 stax-ex-1.7.1
# find stax-ex-1.7.1/ -name '*.jar' -delete
# tar czf stax-ex-1.7.1.tar.gz stax-ex-1.7.1
Source0: %{name}-%{version}.tar.gz

BuildRequires: bea-stax
BuildRequires: dos2unix
BuildRequires: java-devel
BuildRequires: jpackage-utils
BuildRequires: junit
BuildRequires: jvnet-parent
BuildRequires: maven-local
BuildRequires: maven-enforcer-plugin

Requires: bea-stax
Requires: jpackage-utils

BuildArch: noarch


%description
This project develops a few extensions to complement JSR-173 StAX API in the
following area.

* Enable parser instance reuse (which is important in the
  high-performance environment like JAXB and JAX-WS)
* Improve the support for reading from non-text XML infoset,
  such as FastInfoset.
* Improve the namespace support.


%package javadoc
Group: Documentation
Summary: Javadoc for %{name}
Requires: jpackage-utils


%description javadoc
This package contains javadoc for %{name}.


%prep
%setup -q
%pom_remove_dep javax.activation:activation

# Convert the license to UTF-8:
mv LICENSE.txt LICENSE.txt.tmp
iconv -f ISO-8859-1 -t UTF-8 LICENSE.txt.tmp > LICENSE.txt
dos2unix LICENSE.txt


%build
mvn-rpmbuild \
  -Dproject.build.sourceEncoding=UTF-8 \
  install \
  javadoc:aggregate


%install

# Jar files:
install -d -m 755 %{buildroot}%{_javadir}
install -m 644 target/stax-ex-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

# POM files:
install -d -m 755 %{buildroot}%{_mavenpomdir}
cp -p pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom

# Javadoc files:
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -rp target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}

# Dependencies map:
%add_maven_depmap JPP-%{name}.pom %{name}.jar


%files
%{_javadir}/*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*
%doc LICENSE.txt


%files javadoc
%{_javadocdir}/%{name}
%doc LICENSE.txt


%changelog
* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.7.1-3
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Tue Oct 30 2012 Marek Goldmann <mgoldman@redhat.com> - 1.7.1-2
- Added maven-enforcer-plugin BR

* Tue Aug 28 2012 gil cattaneo <puntogil@libero.it> 1.7.1-1
- Updated to upstream version 1.7.1

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Mar 9 2012 Juan Hernandez <juan.hernandez@redhat.com> 1.7-1
- Updated to upstream version 1.7

* Fri Mar 9 2012 Juan Hernandez <juan.hernandez@redhat.com> 1.4-2
- Cleanup of the spec file

* Sat Jan 21 2012 Marek Goldmann <mgoldman@redhat.com> 1.4-1
- Initial packaging
