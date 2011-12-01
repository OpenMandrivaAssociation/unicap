%define lib_major	2
%define lib_name	%mklibname unicap %{lib_major}
%define develname	%mklibname -d unicap

Summary: Library to access different kinds of ( video ) capture devices 
Name: unicap
Version: 0.9.5
Release: %mkrel 4
Source0: http://www.unicap-imaging.org/downloads/%{name}-%{version}.tar.gz
# (fc) 0.9.1-1mdv fix undefined linking error
Patch0: unicap-0.9.1-fixbuild.patch
# (fc) 0.9.1-1mdv build plugin as unversioned module
Patch1: unicap-0.9.3-module.patch
Patch2: unicap-0.9.6-v4l1.patch
License: GPLv2+
Group: System/Libraries
Url: http://www.unicap-imaging.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot
BuildRequires: gtk+2-devel libraw1394-devel libxv-devel
BuildRequires: automake gtk-doc
Buildrequires: intltool
BuildRequires: libalsa-devel
BuildRequires: libtheora-devel >= 1.0
BuildRequires: libvorbis-devel >= 1.2.0

%description
unicap is a library to access different kinds of ( video ) capture devices. 

%package -n %{lib_name}
Summary:	Dynamic libraries for Unicap
Group:		%{group}

%description -n %{lib_name}
unicap is a library to access different kinds of ( video ) capture devices. 

%package -n %{develname}
Summary:	Static libraries, include files for Unicap
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Requires:	%{lib_name} = %{version}
Obsoletes:	%{lib_name}-devel < %{version}
Obsoletes:	%{name}-devel < %{version}

%description -n %{develname}
Static library and headers file
needed in order to develop applications using unicap.

%prep
%setup -q 
%patch0 -p1 -b .undefined
%patch1 -p1 -b .module
%patch2 -p0 -b .v4l

#needed by patch0 
autoreconf -fi

%build

%configure2_5x --disable-v4l
%make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std

#remove unpackaged files
rm -f $RPM_BUILD_ROOT%{_libdir}/unicap%{lib_major}/{backends,cpi}/*.{la,a} 

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post -n %{lib_name} -p /sbin/ldconfig
%endif
  
%if %mdkversion < 200900
%postun -n %{lib_name} -p /sbin/ldconfig
%endif

%files -n %{lib_name} -f %{name}.lang
%defattr(-,root,root)
%{_libdir}/*.so.%{lib_major}*
%dir %{_libdir}/unicap%{lib_major}
%dir %{_libdir}/unicap%{lib_major}/cpi
%{_libdir}/unicap%{lib_major}/cpi/*.so

%files -n %{develname}
%defattr(-,root,root)
%doc %{_datadir}/gtk-doc/html/libucil
%doc %{_datadir}/gtk-doc/html/libunicap
%doc %{_datadir}/gtk-doc/html/libunicapgtk
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/*.so
%attr(644,root,root) %{_libdir}/*.la
%{_libdir}/*.a


