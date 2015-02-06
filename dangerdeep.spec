%define title           Danger from the deep
%define longtitle       WW2 german submarine simulation

Name:		dangerdeep
Version:	0.3.0
Release:	4
Summary:	WW2 german submarine simulation
License:	GPLv2
Group:		Games/Other
URL:		http://dangerdeep.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/dangerdeep/%{name}-%{version}.tar.bz2

Patch0:		%{name}-0.3.0-scons.patch
Patch1:		dangerdeep-0.3.0-gcc4.7-patch
BuildRequires:	scons
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(SDL_net)
BuildRequires:	pkgconfig(SDL_image)
BuildRequires:	pkgconfig(SDL_mixer)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	imagemagick
Requires:	    dangerdeep-data 


%description
Danger from the deep (aka dangerdeep) is a Free / Open Source World War II
German submarine simulation. It is currently available for Linux/i386 and
Windows, but since it uses SDL/OpenGL it should be portable to other operating
systems or platforms. (If anyone wishes to port it, please contact us.) This
game is planned as tactical simulation and will be as realistic as our time and
knowledge of physics allows. It's current state is ALPHA, but it is playable.

%prep
%setup -q 
%patch0 -p1
%patch1 -p1

%build
# (tpg) parallel build
procs=`egrep -c ^cpu[0-9]+ /proc/stat ||:`
if [ "$procs" ="0"]; then
	procs=1
fi

scons -j$procs \
    installbindir=%{buildroot}%{_gamesbindir} \
    installdatadir=%{buildroot}%{_gamesdatadir} \
    datadir=%{_gamesdatadir}/%{name} \
    usex86sse=1    

for i in 16 32 48; do
    convert -size ${i}x$i logo.xpm -resize ${i}x$i %{name}-${i}x$i.png
done

%install
scons \
    installbindir=%{buildroot}%{_gamesbindir} \
    installdatadir=%{buildroot}%{_gamesdatadir} \
    datadir=%{_gamesdatadir}/%{name} \
    install

install -d -m 755 %{buildroot}%{_mandir}/man6
install -m 644 doc/man/dangerdeep.6 %{buildroot}%{_mandir}/man6

install -d -m 755 %{buildroot}%{_datadir}/applications
cat >  %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
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
 

%files
%doc ChangeLog CREDITS README INSTALL LICENSE
%{_gamesbindir}/%{name}
%{_mandir}/man6/*
%{_datadir}/applications/mandriva-%{name}.desktop
%{_miconsdir}/*
%{_iconsdir}/*.*
%{_liconsdir}/*


