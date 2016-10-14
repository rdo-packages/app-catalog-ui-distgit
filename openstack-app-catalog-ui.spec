%global service app-catalog-ui

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:         openstack-app-catalog-ui
Version:      XXX
Release:      XXX
Summary:      The UI component for the OpenStack App Catalog

License:      ASL 2.0
URL:          https://github.com/openstack/apps-catalog-ui
Source0:      https://github.com/openstack/%{service}/archive/%{version}.tar.gz#/%{project}-%{upstream_version}.tar.gz

BuildArch:     noarch

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-pbr
BuildRequires: openstack-dashboard

Requires: pytz
Requires: openstack-dashboard
Requires: python-pbr
Requires: python-oslo-config


%description
app-catalog-ui is an OpenStack Horizon user interface plugin to
provide easy access to the OpenStack App Catalog.

%prep
%setup -q -n %{service}-%{upstream_version}

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf tools/{pip,test}-requires
truncate -s 0 {test-,}requirements.txt

%build
export OSLO_PACKAGE_VERSION=%{version}
%{__python2} setup.py build

%install
export OSLO_PACKAGE_VERSION=%{version}
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

# Move config to horizon
mkdir -p  %{buildroot}%{_sysconfdir}/openstack-dashboard/enabled
mkdir -p  %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled
mv app_catalog/enabled/_50_dashboard_catalog.py %{buildroot}%{_sysconfdir}/openstack-dashboard/enabled/_50_dashboard_catalog.py
mv app_catalog/enabled/_51_app_catalog.py %{buildroot}%{_sysconfdir}/openstack-dashboard/enabled/_51_app_catalog.py
mv app_catalog/enabled/_60_panel_group_browse.py %{buildroot}%{_sysconfdir}/openstack-dashboard/enabled/_60_panel_group_browse.py
mv app_catalog/enabled/_61_app_catalog_panel.py %{buildroot}%{_sysconfdir}/openstack-dashboard/enabled/_61_app_catalog_panel.py
mv app_catalog/enabled/_62_project_component_catalog_panel.py %{buildroot}%{_sysconfdir}/openstack-dashboard/enabled/_62_project_component_catalog_panel.py
ln -s %{_sysconfdir}/openstack-dashboard/enabled/_50_dashboard_catalog.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_50_dashboard_catalog.py
ln -s %{_sysconfdir}/openstack-dashboard/enabled/_51_app_catalog.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_51_app_catalog.py
ln -s %{_sysconfdir}/openstack-dashboard/enabled/_60_panel_group_browse.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_60_panel_group_browse.py
ln -s %{_sysconfdir}/openstack-dashboard/enabled/_61_project_app_catalog_panel.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_61_project_app_catalog_panel.py
ln -s %{_sysconfdir}/openstack-dashboard/enabled/_62_project_component_catalog_panel.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_62_project_component_catalog_panel.py

# Move static files to horizon. These require that you compile them again
# post install { python manage.py compress }
mkdir -p  %{buildroot}%{python2_sitelib}/app_catalog/static
mkdir -p  %{buildroot}%{python2_sitelib}/app_catalog/templates
mkdir -p  %{buildroot}%{python2_sitelib}/component_catalog/templates
cp -r app_catalog/static/* %{buildroot}%{python2_sitelib}/app_catalog/static/
cp -r app_catalog/templates/* %{buildroot}%{python2_sitelib}/app_catalog/templates/
rm -rf %{buildroot}%{python2_sitelib}/app_catalog/enabled

%check
# TODO: enable upstream tests

%files
%doc README.rst
%license LICENSE
%dir %{python2_sitelib}/app_catalog
%dir %{python2_sitelib}/component_catalog
%{python2_sitelib}/*.egg-info
%{python2_sitelib}/app_catalog/*.py*
%{python2_sitelib}/app_catalog/templates
%{python2_sitelib}/app_catalog/static
%{python2_sitelib}/app_catalog/tests
%{python2_sitelib}/app_catalog/app_catalog
%{python2_sitelib}/app_catalog/component_catalog/*.py*
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_50_dashboard_catalog.py
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_51_app_catalog.py
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_60_panel_group_browse.py
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_61_project_app_catalog_panel.py
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_62_project_component_catalog_panel.py
%{_sysconfdir}/openstack-dashboard/enabled/_50_dashboard_catalog.py*
%{_sysconfdir}/openstack-dashboard/enabled/_51_app_catalog.py*
%{_sysconfdir}/openstack-dashboard/enabled/_60_panel_group_browse.py*
%{_sysconfdir}/openstack-dashboard/enabled/_61_app_catalog_panel.py*
%{_sysconfdir}/openstack-dashboard/enabled/_62_project_component_catalog_panel.py*

%changelog
