%define name            dangerdeep
%define version         0.2.0
%define release         %mkrel 1
%define title           Danger from the deep
%define longtitle       WW2 german submarine simulation

Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:        WW2 german submarine simulation
License:        GPL
Group:          Games/Other
URL:            http://dangerdeep.sourceforge.net/
Source0:        http://prdownloads.sourceforge.net/dangerdeep/%{name}-%{version}.tar.bz2
Buildrequires:  scons
Buildrequires:  fftw-devel
Buildrequires:  SDL-devel
Buildrequires:  SDL_net-devel
Buildrequires:  SDL_image-devel
Buildrequires:  SDL_mixer-devel
Buildrequires:  mesaglu-devel
Buildrequires:  ImageMagick
Requires:       dangerdeep-data
BuildRoot:      %_tmppath/%{name}-%{version}

%description
Danger from the deep (aka dangerdeep) is a Free / Open Source World War II
german submarine simulation. It is currently available for Linux/i386 and
Windows, but since it uses SDL/OpenGL it should be portable to other operating
systems or platforms. (If anyone whishes to port it, please contact us.) This
game is planned as tactical simulation and will be as realistic as our time and
knowledge of physics allows. It's current state is ALPHA, but it is playable.

%prep
%setup -q
perl -pi \
    -e 's|/usr/local/bin|%_gamesbindir|;' \
    -e 's|/usr/local/share/dangerdeep|%_gamesdatadir/dangerdeep|;' \
    SConstruct

%build
scons -k
for i in 16 32 48; do
    convert -size ${i}x$i logo.xpm -resize ${i}x$i %{name}-${i}x$i.png
done

%install
rm -rf %{buildroot}

install -d -m 755 %{buildroot}%{_gamesbindir}
install -m 755 build/linux/%{name} %{buildroot}%{_gamesbindir}

install -d -m 755 %{buildroot}%{_mandir}/man6
install -m 644 doc/man/dangerdeep.6 %{buildroot}%{_mandir}/man6

install -d -m 755 %{buildroot}%{_datadir}/applications
cat >  %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=%{title}
Comment=%{longtitle}
Exec=%{_gamesbindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=false
Categories=X-MandrivaLinux-MoreApplications-Games-Other;Game;
EOF
  
# icon
install -d -m 755 %{buildroot}/%{_miconsdir}
install -d -m 755 %{buildroot}/%{_iconsdir}
install -d -m 755 %{buildroot}/%{_liconsdir}
install -m 644 %{name}-16x16.png %{buildroot}/%{_miconsdir}/%{name}.png
install -m 644 %{name}-32x32.png %{buildroot}/%{_iconsdir}/%{name}.png
install -m 644 %{name}-48x48.png %{buildroot}/%{_liconsdir}/%{name}.png
 
%post
%{update_menus}

%postun
%{clean_menus}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ChangeLog CREDITS README INSTALL LICENSE
%{_gamesbindir}/*
%{_mandir}/man6/*
%{_datadir}/applications/mandriva-%{name}.desktop
%{_miconsdir}/*
%{_iconsdir}/*.*
%{_liconsdir}/*


