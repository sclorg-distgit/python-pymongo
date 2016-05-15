%{?scl:%scl_package python-pymongo}
%{!?scl:%global pkg_name %{name}}

# Fix private-shared-object-provides error
# Also fix overrided requires for python(abi)
#%{?scl:%filter_provides_in %{python3_sitearch}.*\.so$}
#%{?scl:%filter_from_requires s|python(abi)|%{?scl_prefix}python(abi)|g}
#%{?scl:%filter_setup}

Name:           %{?scl_prefix}python-pymongo
Version:        3.2.1
Release:        2%{?dist}
Summary:        Python driver for MongoDB

Group:          Development/Languages
# All code is ASL 2.0 except bson/time64*.{c,h} which is MIT
License:        ASL 2.0 and MIT
URL:            http://api.mongodb.org/python
Source0:        https://github.com/mongodb/mongo-python-driver/archive/%{version}.tar.gz
Patch01:        0001-Serverless-test-suite-workaround.patch
BuildRoot:      %{_tmppath}/%{pkg_name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       %{?scl_prefix}python-bson = %{version}-%{release}

BuildRequires:  %{?scl_prefix}python-devel
BuildRequires:  %{?scl_prefix}python-nose
BuildRequires:  %{?scl_prefix}python-setuptools
BuildRequires:  %{?scl_prefix}python-sphinx
%{?scl:Requires: %scl_runtime}

# Mongodb must run on a little-endian CPU (see bug #630898)
ExcludeArch:    ppc ppc64 %{sparc} s390 s390x

%description
The Python driver for MongoDB.

%package doc
Summary: Documentation for python-pymongo


%description doc
Documentation for python-pymongo.

%package gridfs
Summary:        Python GridFS driver for MongoDB
Group:          Development/Libraries
Requires:       %{?scl_prefix}%{pkg_name}%{?_isa} = %{version}-%{release}

%description gridfs
GridFS is a storage specification for large objects in MongoDB.

%package -n %{?scl_prefix}python-bson
Summary:        Python bson library
Group:          Development/Libraries

%description -n %{?scl_prefix}python-bson
BSON is a binary-encoded serialization of JSON-like documents. BSON is designed
to be lightweight, traversable, and efficient. BSON, like JSON, supports the
embedding of objects and arrays within other objects and arrays.

%prep
%setup -q -n mongo-python-driver-%{version}
%patch01 -p1 -b .test

%build
%{?scl:scl enable %{scl} - << \EOF}
CFLAGS="%{optflags}" %{__python3} setup.py build
pushd doc
make html
popd
%{?scl:EOF}

%install
rm -rf %{buildroot}
%{?scl:scl enable %{scl} - << \EOF}
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
chmod 755 %{buildroot}%{python3_sitearch}/bson/*.so
chmod 755 %{buildroot}%{python3_sitearch}/pymongo/*.so
%{?scl:EOF}

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root,-)
%doc LICENSE README.rst doc
%{python3_sitearch}/pymongo
%{python3_sitearch}/pymongo-%{version}-*.egg-info

%files gridfs
%defattr(-,root,root,-)
%doc LICENSE README.rst doc
%{python3_sitearch}/gridfs

%files -n %{?scl_prefix}python-bson
%defattr(-,root,root,-)
%doc LICENSE README.rst doc
%{python3_sitearch}/bson

%files doc
%defattr(-,root,root,-)
%doc LICENSE
%doc doc/_build/html/*

%check
# Exclude tests that require an active MongoDB connection
 exclude='(^test_auth_from_uri$'
exclude+='|^test_auto_auth_login$'
exclude+='|^test_auto_reconnect_exception_when_read_preference_is_secondary$'
exclude+='|^test_auto_start_request$'
exclude+='|^test_binary$'
exclude+='|^test_client$'
exclude+='|^test_collection$'
exclude+='|^test_common$'
exclude+='|^test_config_ssl$'
exclude+='|^test_connect$'
exclude+='|^test_connection$'
exclude+='|^test_constants$'
exclude+='|^test_contextlib$'
exclude+='|^test_copy_db$'
exclude+='|^test_cursor$'
exclude+='|^test_crud$'
exclude+='|^test_database$'
exclude+='|^test_database_names$'
exclude+='|^test_delegated_auth$'
exclude+='|^test_disconnect$'
exclude+='|^test_discovery_and_monitoring$'
exclude+='|^test_document_class$'
exclude+='|^test_drop_database$'
exclude+='|^test_equality$'
exclude+='|^test_fork$'
exclude+='|^test_from_uri$'
exclude+='|^test_fsync_lock_unlock$'
exclude+='|^test_get_db$'
exclude+='|^test_getters$'
exclude+='|^test_grid_file$'
exclude+='|^test_gridfs$'
exclude+='|^test_host_w_port$'
exclude+='|^test_interrupt_signal$'
exclude+='|^test_ipv6$'
exclude+='|^test_iteration$'
exclude+='|^test_json_util$'
exclude+='|^test_kill_cursor_explicit_primary$'
exclude+='|^test_kill_cursor_explicit_secondary$'
exclude+='|^test_master_slave_connection$'
exclude+='|^test_nested_request$'
exclude+='|^test_network_timeout$'
exclude+='|^test_network_timeout_validation$'
exclude+='|^test_operation_failure_with_request$'
exclude+='|^test_operation_failure_without_request$'
exclude+='|^test_operations$'
exclude+='|^test_pinned_member$'
exclude+='|^test_pooling$'
exclude+='|^test_pooling_gevent$'
exclude+='|^test_properties$'
exclude+='|^test_pymongo$'
exclude+='|^test_read_preferences$'
exclude+='|^test_replica_set_client$'
exclude+='|^test_replica_set_connection$'
exclude+='|^test_replica_set_connection_alias$'
exclude+='|^test_repr$'
exclude+='|^test_request_threads$'
exclude+='|^test_safe_insert$'
exclude+='|^test_safe_update$'
exclude+='|^test_schedule_refresh$'
exclude+='|^test_server_disconnect$'
exclude+='|^test_server_selection$'
exclude+='|^test_server_selection_rtt$'
exclude+='|^test_son_manipulator$'
exclude+='|^test_threading$'
exclude+='|^test_threads$'
exclude+='|^test_threads_replica_set_connection$'
exclude+='|^test_timeouts$'
exclude+='|^test_tz_aware$'
exclude+='|^test_uri_options$'
exclude+='|^test_use_greenlets$'
exclude+='|^test_with_start_request$'
exclude+='|^test_command_monitoring_spec$'
exclude+='|^test_gridfs_spec$'
exclude+='|^test_uri_spec$'
exclude+='|^test_legacy_api$'
exclude+='|^test_raw_bson$'
exclude+=')'
%{?scl:scl enable %{scl} '}
pushd test
nosetests --exclude="$exclude"
popd
%{?scl:'}

%changelog
* Wed Apr 27 2016 Charalampos Stratakis <cstratak@redhat.com - 3.2.1-2
- Changed license tag to doc tag for the LICENSE file in the doc subpackage
Resolves: rhbz#1330597

* Sat Feb 13 2016 Robert Kuska <rkuska@redhat.com> - 3.2.1-1
- Update to 3.2.1

* Thu Jan 22 2015 Robert Kuska <rkuska@redhat.com> - 2.7.2-1
- Update to 2.7.2

* Tue Oct 15 2013 Robert Kuska <rkuska@redhat.com> - 2.5.2-4
- Rebuilt for scl

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 13 2013 Andrew McNabb <amcnabb@mcnabbs.org> - 2.5.2-2
- Bump the obsoletes version for pymongo-gridfs

* Wed Jun 12 2013 Andrew McNabb <amcnabb@mcnabbs.org> - 2.5.2-1
- Update to pymongo 2.5.2

* Tue Jun 11 2013 Andrew McNabb <amcnabb@mcnabbs.org> - 2.5-5
- Bump the obsoletes version

* Wed Apr 24 2013 Andrew McNabb <amcnabb@mcnabbs.org> - 2.5-4
- Fix the test running procedure

* Wed Apr 24 2013 Andrew McNabb <amcnabb@mcnabbs.org> - 2.5-3
- Exclude tests in pymongo 2.5 that depend on MongoDB

* Mon Apr 22 2013 Andrew McNabb <amcnabb@mcnabbs.org> - 2.5-1
- Update to PyMongo 2.5 (bug #954152)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jan  5 2013 Andrew McNabb <amcnabb@mcnabbs.org> - 2.3-6
- Fix dependency of python3-pymongo-gridfs (bug #892214)

* Tue Nov 27 2012 Andrew McNabb <amcnabb@mcnabbs.org> - 2.3-5
- Fix the name of the python-pymongo-gridfs subpackage

* Tue Nov 27 2012 Andrew McNabb <amcnabb@mcnabbs.org> - 2.3-4
- Fix obsoletes for python-pymongo-gridfs subpackage

* Tue Nov 27 2012 Andrew McNabb <amcnabb@mcnabbs.org> - 2.3-3
- Fix requires to include the arch, and add docs to all subpackages

* Tue Nov 27 2012 Andrew McNabb <amcnabb@mcnabbs.org> - 2.3-2
- Remove preexisting egg-info

* Mon Nov 26 2012 Andrew McNabb <amcnabb@mcnabbs.org> - 2.3-1
- Rename, update to 2.3, and add support for Python 3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 10 2012 Silas Sewell <silas@sewell.org> - 2.1.1-1
- Update to 2.1.1

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jul 24 2011 Silas Sewell <silas@sewell.org> - 1.11-1
- Update to 1.11

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov 18 2010 Dan Horák <dan[at]danny.cz> - 1.9-5
- add ExcludeArch to match mongodb package

* Tue Oct 26 2010 Silas Sewell <silas@sewell.ch> - 1.9-4
- Add comment about multi-license

* Thu Oct 21 2010 Silas Sewell <silas@sewell.ch> - 1.9-3
- Fixed tests so they actually run
- Change python-devel to python2-devel

* Wed Oct 20 2010 Silas Sewell <silas@sewell.ch> - 1.9-2
- Add check section
- Use correct .so filter
- Added python3 stuff (although disabled)

* Tue Sep 28 2010 Silas Sewell <silas@sewell.ch> - 1.9-1
- Update to 1.9

* Tue Sep 28 2010 Silas Sewell <silas@sewell.ch> - 1.8.1-1
- Update to 1.8.1

* Sat Dec 05 2009 Silas Sewell <silas@sewell.ch> - 1.1.2-1
- Initial build
