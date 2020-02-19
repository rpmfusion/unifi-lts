# This is a binary package so debuginfo doesn't do anything useful.
%global debug_package %{nil}
%define __jar_repack %{nil}
%global __strip /bin/true

Name:           unifi-lts
Version:        5.6.42
Release:        5%{?dist}
Summary:        Ubiquiti UniFi controller LTS

License:        Proprietary
URL:            https://unifi-sdn.ubnt.com/
Source0:        http://dl.ubnt.com/unifi/%{version}/UniFi.unix.zip#/UniFi-%{version}.unix.zip
Source1:        unifi.service
Source3:        unifi.xml
Source4:        unifi.logrotate
Source5:        unifi.sh
Source6:        mongod.sh
Source100:      PERMISSION-1.html
Source101:      PERMISSION-2.html
Source102:      SETUP


BuildRequires:  systemd
%{?systemd_requires}
Requires(pre):  shadow-utils
Requires:       firewalld-filesystem
BuildRequires:  firewalld-filesystem
BuildRequires:  %{_bindir}/execstack

# https://fedoraproject.org/wiki/Changes/MongoDB_Removal
#Requires:       /usr/bin/mongod
Requires:       java-headless = 1:1.8.0

%if 0%{?rhel} && 0%{?rhel} < 8
Requires(post): policycoreutils-python
Requires(postun): policycoreutils-python
%else
Requires(post): policycoreutils-python-utils
Requires(postun): policycoreutils-python-utils
%endif

# Unbundled fonts
Requires:       fontawesome-fonts
Requires:       fontawesome-fonts-web

# Prevent other versions of unifi from being installed.
Conflicts:      unifi unifi-controller

# https://bugzilla.redhat.com/show_bug.cgi?id=1517565
Provides:       bundled(lato-fonts-web)
Provides:       bundled(ubnt-fonts)

# Bundled java libraries
# This needs to be automated!
Provides:       bundled(commons-io) = 2.4
Provides:       bundled(compiler) = 0.8.18
Provides:       bundled(commons-logging) = 1.1.3
Provides:       bundled(commons-codec) = 1.7
Provides:       bundled(httpcore) = 4.2
Provides:       bundled(commons-validator) = 1.5.0
Provides:       bundled(spring-core) = 3.2.8
Provides:       bundled(aws-java-sdk-core) = 1.9.3
Provides:       bundled(urlrewritefilter) = 4.0.4
Provides:       bundled(jorbis) = 0.0.17
Provides:       bundled(spring-expression) = 3.2.8
Provides:       bundled(sshj) = 0.9.0
Provides:       bundled(mail) = 1.4.7
Provides:       bundled(commons-lang) = 2.6
Provides:       bundled(radclient4)
Provides:       bundled(spring-context) 3.2.8
Provides:       bundled(cron4j) = 2.2.5
Provides:       bundled(tomcat-annotations-api) = 7.0.82
Provides:       bundled(jmdns) = 3.4.1
Provides:       bundled(mongo-java-driver) = 2.14.3
Provides:       bundled(httpclient) = 4.2
Provides:       bundled(slf4j-log4j12) = 1.7.6
Provides:       bundled(dom4j) = 1.3
Provides:       bundled(spring-beans) = 3.2.8
Provides:       bundled(jackson-annotations) = 2.1.1
Provides:       bundled(aws-java-sdk-cloudwatch) = 1.9.3
Provides:       bundled(annotations) = 2.0.0
Provides:       bundled(snappy-java) = 1.1.2.6
Provides:       bundled(tomcat-embed-logging-juli) = 7.0.82
Provides:       bundled(commons-beanutils) = 1.9.1
Provides:       bundled(tomcat-embed-core) =  7.0.82
Provides:       bundled(tomcat-embed-jasper) = 7.0.82
Provides:       bundled(jstl) = 1.2
Provides:       bundled(aws-java-sdk-s3) = 1.9.3
Provides:       bundled(servo-core) = 0.9.4
Provides:       bundled(log4j) = 1.2.17
Provides:       bundled(slf4j-api) = 1.7.6
Provides:       bundled(commons-net) = 3.3
Provides:       bundled(commons-httpclient-contrib) = 3.1
Provides:       bundled(jul-to-slf4j) = 1.7.6
Provides:       bundled(gson) = 2.2.4
Provides:       bundled(jstun) = 0.7.3
Provides:       bundled(Java-WebSocket) = 1.3.0
Provides:       bundled(jackson-databind) = 2.1.1
Provides:       bundled(commons-httpclient) = 3.1
Provides:       bundled(spring-test) = 3.2.8
Provides:       bundled(tomcat-embed-logging-log4j) = 7.0.82
Provides:       bundled(commons-pool2) = 2.2
Provides:       bundled(jsch) = 0.1.51
Provides:       bundled(joda-time) = 2.9.4
Provides:       bundled(jackson-core) = 2.1.1
Provides:       bundled(guava) = 14.0.1
Provides:       bundled(ecj) = 4.3.1
Provides:       bundled(jedis) = 2.8.1
Provides:       bundled(tomcat-embed-el) = 7.0.82
Provides:       bundled(servo-graphite) = 0.9.4

# So you can prevent automatic updates.
%if 0%{?fedora}
Recommends:     dnf-plugin-versionlock
%endif

Requires:       unifi-lts-data = %{version}-%{release}


%description
Ubiquiti UniFi server is a centralized management system for UniFi suite of
devices. After the UniFi server is installed, the UniFi controller can be
accessed on any web browser. The UniFi controller allows the operator to
instantly provision thousands of UniFi devices, map out network topology,
quickly manage system traffic, and further provision individual UniFi devices.

This is the Long Term Support (LTS) package which also supports Gen 1 APs.


%package data
BuildArch:      noarch
Summary:        Non-architechture specific data files for unifi

%description data
Non-architechture specific data files for the unifi controller software.


%prep
%autosetup -n UniFi

install -pm 0644 %{SOURCE102} .

# Unbundle fontawesome fot
rm -f webapps/ROOT/app-unifi/fonts/*.{ttf,eot,otf,svg,woff,woff2}


%install
# Install into /usr/share/unifi
mkdir -p %{buildroot}%{_datadir}/unifi
cp -a ./*  %{buildroot}%{_datadir}/unifi/

# Remove readme as it will be handled by %%doc
rm -f %{buildroot}%{_datadir}/unifi/readme.txt

### Attempt a more FHS compliant install...
# Create directories for live data and symlink it into /usr/share so unifi
# can find them.
mkdir -p %{buildroot}%{_sharedstatedir}/unifi/{data,run,work}
ln -sr %{buildroot}%{_sharedstatedir}/unifi/data \
       %{buildroot}%{_datadir}/unifi/data
ln -sr %{buildroot}%{_sharedstatedir}/unifi/run \
       %{buildroot}%{_datadir}/unifi/run
ln -sr %{buildroot}%{_sharedstatedir}/unifi/work \
       %{buildroot}%{_datadir}/unifi/work

# Create logs in /var/log and symlink it in.
mkdir -p %{buildroot}%{_localstatedir}/log/unifi
ln -sr %{buildroot}%{_localstatedir}/log/unifi \
       %{buildroot}%{_datadir}/unifi/logs

# Install systemd service file
install -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/unifi.service

# Install firewalld config
mkdir -p %{buildroot}%{_prefix}/lib/firewalld/services
install -pm 0644 %{SOURCE3} %{buildroot}%{_prefix}/lib/firewalld/services/

# Remove non-native executables
rm -rf %{buildroot}%{_datadir}/unifi/lib/native/{Windows,Mac}

# webrtc is only supported on x86_64, aarch64 and armv7hf.
# Move libraries to the correct location and symlink back
mkdir -p %{buildroot}%{_libdir}
mv %{buildroot}%{_datadir}/unifi/lib/native/Linux ./
%ifarch x86_64 armv7hl
# Set the correct arch for the webrtc library.
%ifarch armv7hl
%global unifi_arch armhf
%else 
%global unifi_arch %{_target_cpu}
%endif
mkdir -p %{buildroot}%{_datadir}/unifi/lib/native/Linux/%{unifi_arch}
mv Linux/%{unifi_arch}/libubnt_webrtc_jni.so %{buildroot}%{_libdir}/
ln -sr %{buildroot}%{_libdir}/libubnt_webrtc_jni.so \
       %{buildroot}%{_datadir}/unifi/lib/native/Linux/%{unifi_arch}

# Try to fix java VM warning about running execstack on libubnt_webrtc_jni.so
find %{buildroot}%{_libdir} -name libubnt_webrtc_jni.so -exec execstack -c {} \;
%endif

# Install logrotate config
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
install -pm 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/logrotate.d/unifi

# Install wrapper script for java to workaround lack of $ORIGIN when executed
# directly.
mkdir -p %{buildroot}%{_sbindir}
install %{SOURCE5} %{buildroot}%{_sbindir}/unifi

# Install forum messages giving permission to redistribute.
install -p %{SOURCE100} %{SOURCE101} .

#
# Workaround script for MongoDB 3.6 no longer accepting --nohttpinterface.
# See: https://community.ubnt.com/t5/UniFi-Routing-Switching/MongoDB-3-6/m-p/2322445#M86254
#
install -pm 0755 %{SOURCE6} %{buildroot}%{_datadir}/unifi/bin/mongod


%pre
getent group unifi >/dev/null || groupadd -r unifi
getent passwd unifi >/dev/null || \
    useradd -r -g unifi -d %{_sharedstatedir}/unifi -s /sbin/nologin \
    -c "Ubiquitu UniFi Controller" unifi
exit 0

%post
%systemd_post unifi.service
%{?firewalld_reload}

# Set required SELinux context for unifi to use a private mongodb database.
%if "%{_selinux_policy_version}" != ""
    semanage fcontext -a -t mongod_log_t \
        "%{_localstatedir}/log/unifi(/.*)?" 2>/dev/null || :
    semanage fcontext -a -t mongod_var_lib_t \
        "%{_sharedstatedir}/unifi/data(/.*)?" 2>/dev/null || :
    restorecon -R %{_localstatedir}/log/unifi \
                  %{_sharedstatedir}/unifi/data || :
    semanage port -a -t mongod_port_t -p tcp 27117 2>/dev/null || :
%endif

%firewalld_reload


%preun
%systemd_preun unifi.service

%postun
# Restart the service on upgrade.
%systemd_postun_with_restart unifi.service
# Remove selinux modifications on uninstall
if [ $1 -eq 0 ] ; then  # final removal
%if "%{_selinux_policy_version}" != ""
    semanage fcontext -d -t mongod_log_t \
        "%{_localstatedir}/log/unifi(/.*)?" 2>/dev/null || :
    semanage fcontext -d -t mongod_var_lib_t \
        "%{_sharedstatedir}/unifi/data(/.*)?" 2>/dev/null || :
    semanage port -d -t mongod_port_t -p tcp 27117 2>/dev/null || :
%endif
fi


%files
%doc readme.txt SETUP
%license PERMISSION*.html
%ifarch x86_64 armv7hl
%{_libdir}/libubnt_webrtc_jni.so
%{_datadir}/unifi/lib/native/
%endif
%{_datadir}/unifi/bin/mongod
%{_sbindir}/unifi
%{_sysconfdir}/logrotate.d/unifi
%{_unitdir}/unifi.service
%{_prefix}/lib/firewalld/services/unifi.xml
%ghost %attr(-,unifi,unifi) %config(missingok,noreplace) %{_sharedstatedir}/unifi/data/system.properties
%attr(-,unifi,unifi) %{_localstatedir}/log/unifi/
%dir %attr(-,unifi,unifi) %{_sharedstatedir}/unifi
%dir %attr(-,unifi,unifi) %{_sharedstatedir}/unifi/data
%dir %attr(-,unifi,unifi) %{_sharedstatedir}/unifi/run
%dir %attr(-,unifi,unifi) %{_sharedstatedir}/unifi/work

%files data
%exclude %{_datadir}/unifi/lib/native
%exclude %{_datadir}/unifi/bin/mongod
%{_datadir}/unifi/


%changelog
* Wed Feb 19 2020 Richard Shaw <hobbes1069@gmail.com> - 5.6.42-5
- Really fix requires for policycoreutils-python on EL 7.

* Tue Feb 18 2020 Richard Shaw <hobbes1069@gmail.com> - 5.6.42-4
- Fix Requires for EL 7, fixes RFBZ#5531.

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 5.6.42-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Oct 14 2019 Richard Shaw <hobbes1069@gmail.com> - 5.6.42-3
- Remove hard dependency on mongodb and document in SETUP.
- Fix Requires for java to comply with guidelines.
- Try JAVA_HOME instead of forcing java 1.8.0 via alternatives.

* Sat Aug 10 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 5.6.42-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat May 04 2019 Richard Shaw <hobbes1069@gmail.com> - 5.6.42-1
- Update to 5.6.42.

* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 5.6.40-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Sep 21 2018 Richard Shaw <hobbes1069@gmail.com> - 5.6.40-1
- Initial packaging of LTS version.

