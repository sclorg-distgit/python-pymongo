%{?scl:%scl_package python-pymongo}
%{!?scl:%global pkg_name %{name}}

# Fix private-shared-object-provides error
# Also fix overrided requires for python(abi)
#%{?scl:%filter_provides_in %{python3_sitearch}.*\.so$}
#%{?scl:%filter_from_requires s|python(abi)|%{?scl_prefix}python(abi)|g}
#%{?scl:%filter_setup}

Name:           %{?scl_prefix}python-pymongo
Version:        3.4.0
Release:        1%{?dist}
Summary:        Python driver for MongoDB

Group:          Development/Languages
# All code is ASL 2.0 except bson/time64*.{c,h} which is MIT
License:        ASL 2.0 and MIT
URL:            http://api.mongodb.org/python
Source0:        https://github.com/mongodb/mongo-python-driver/archive/%{version}.tar.gz

# This patch removes the bundled ssl.match_hostname library as it was vulnerable to CVE-2013-7440
# and CVE-2013-2099, and wasn't needed anyway since the needed module is in the Python
# standard library now. It also adjusts imports so that they exclusively use the code from Python.
Patch01:        0001-Use-ssl.match_hostname-from-the-Python-stdlib.patch

Patch02:        0002-Serverless-test-suite-workaround.patch

# Patch: PYTHON-1216 Tests should pass without MongoDB running
# From upstram, should be included in the next released version:
# - https://github.com/mongodb/mongo-python-driver/commit/6142f761e7ad7807eba0c5fcdbad78bfe364b01a
Patch03:        0003-PYTHON-1216-Tests-should-pass-without-MongoDB-running.patch

BuildRoot:      %{_tmppath}/%{pkg_name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       %{?scl_prefix}python-bson = %{version}-%{release}

BuildRequires:  %{?scl_prefix}python-devel
BuildRequires:  %{?scl_prefix}python-setuptools
BuildRequires:  %{?scl_prefix}python-sphinx
%{?scl:Requires: %scl_runtime}

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

%patch01 -p1 -b .ssl
%patch02 -p1 -b .test
%patch03 -p1

# Remove the bundled ssl.match_hostname library as it was vulnerable to CVE-2013-7440
# and CVE-2013-2099, and isn't needed anyway since the needed module is in the Python
# standard library now.
rm pymongo/ssl_match_hostname.py


%build
%{?scl:scl enable %{scl} - << \EOF}
CFLAGS="%{optflags}" %{__python3} setup.py build

pushd doc
make %{?_smp_mflags} html
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
%{?scl:scl enable %{scl} '}
python3 setup.py test
%{?scl:'}

%changelog
* Fri Jun 16 2017 Tomas Orsava <torsava@redhat.com> - 3.4.0-1
- Updated to the latest Fedora version 3.4.0
- Renumbered Patch 1 to 2 to be in line with Fedora
- Added Patch 1 from Fedora that fixes CVE-2013-7440 and CVE-2013-2099
- Added Patch 3 from upstream for tests to pass without an active mongodb;
  We can't test pymongo with a running database like in Fedora, because in
  RHEL/RHSCLs it's packaged as a separate collection
- Removed BuildRequires: python-nose as the test suite isn't using it any more

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
