Name:           ojuba-desktop-settings
Version:        5.0.3
Release:        1%{dist}
Summary:        Ojuba desktop default settings
Group:          User Interface/Desktops
License:        Waqf
URL:            http://www.ojuba.org/
Source0:        http://git.ojuba.org/cgit/%{name}/snapshot/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
Provides:	ojuba-gnome-settings
Obsoletes:      ojuba-gnome-settings<%{version}-%{release}
Requires(post): glib2
# Requires(post):	google-release, skype-release
# Requires(post): notification-daemon-engine-nodoka

%description
Ojuba desktop default settings.

%prep
%setup -q

%build
%install
%{__rm} -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/
cp -a etc usr var $RPM_BUILD_ROOT/


%post
/usr/bin/glib-compile-schemas /usr/share/glib-2.0/schemas/
gconftool-2 --direct --config-source=xml:readwrite:/etc/gconf/gconf.xml.defaults -s /apps/metacity/general/titlebar_font --type string 'Sans 11'

%postun
/usr/bin/glib-compile-schemas /usr/share/glib-2.0/schemas/
gconftool-2 --direct --config-source=xml:readwrite:/etc/gconf/gconf.xml.defaults -s /apps/metacity/general/titlebar_font --type string 'Cantarell Bold 11'

%files
%config(noreplace) /etc/X11/xorg.conf.d/00-touchpad.conf
%config(noreplace) /etc/X11/xinit/xinitrc.d/xim4arabic.sh
%config(noreplace) /etc/modprobe.d/*
%config(noreplace) /etc/profile.d/*
%config(noreplace) /etc/fonts/conf.d/*
%config(noreplace) /etc/fonts/conf.avail/*
%config(noreplace) /etc/skel/.mplayer/config
%{_datadir}/glib-2.0/schemas/*.override
/var/lib/polkit-1/localauthority/10-vendor.d/*


%changelog
* Fri Jul 29 2011  Muayyad Saleh Alsadi <alsadi@ojuba.org> - 5.0.0-3
- update to use gsettings
- obsolete ojuba-gnome-settings

* Wed Jul 28 2010  Muayyad Saleh Alsadi <alsadi@ojuba.org> - 4.0.0-5
- update to use new wallpaper

* Wed Jun 30 2010  Muayyad Saleh Alsadi <alsadi@ojuba.org> - 4.0.0-4
- replace oo.o quick launch icon with occ's

* Fri Jun 18 2010  Muayyad Saleh Alsadi <alsadi@ojuba.org> - 4.0.0-3
- remove StickyNotesApplet KeyboardApplet

* Thu Jun 17 2010  Muayyad Saleh Alsadi <alsadi@ojuba.org> - 4.0.0-2
- update for ojuba 4

* Sat Aug 22 2009  Muayyad Saleh Alsadi <alsadi@ojuba.org> - 2.0.0-1
- Arabic Italic to the right

* Tue Jul 21 2009  Muayyad Saleh Alsadi <alsadi@ojuba.org> - 1.3.0-1
- rebuild for ojuba 3

* Tue Jul 14 2009  Muayyad Saleh Alsadi <alsadi@ojuba.org> - 1.2.0-1
- update fontconfigs

* Tue Jan 27 2009  Muayyad Saleh Alsadi <alsadi@ojuba.org> - 1.1.0-4
- disable pc speaker

* Thu Jan 22 2009  Muayyad Saleh Alsadi <alsadi@ojuba.org> - 1.1.0-3
- add %%config 

* Tue Jan 20 2009  Muayyad Saleh Alsadi <alsadi@ojuba.org> - 1.1.0-2
- default configuration for mplayer

* Sun Jan 18 2009  Muayyad Saleh Alsadi <alsadi@ojuba.org> - 1.1.0-1
- new font configuration

* Wed Dec 31 2008   Muayyad Saleh Alsadi <alsadi@ojuba.org> - 1.0.0-10
- use notification-daemon-engine-nodoka

* Sat Jun 28 2008   Muayyad Saleh Alsadi <alsadi@ojuba.org> - 1.0.0-9
- set default totem backend
- remove shade windows with double click on title bar
- drop the need for boot-i18n
- do not disable compiz-fusion-release
* Sat Jun 28 2008   Muayyad Saleh Alsadi <alsadi@ojuba.org> - 1.0.0-8
- fix small bug

* Sat Jun 28 2008   Muayyad Saleh Alsadi <alsadi@ojuba.org> - 1.0.0-7
- disable extra repos like google-release, skype-release, compiz-fusion-release

* Sat Jun 28 2008   Muayyad Saleh Alsadi <alsadi@ojuba.org> - 1.0.0-6
- disable dict.cn in stardict

* Sat Jun 28 2008   Muayyad Saleh Alsadi <alsadi@ojuba.org> - 1.0.0-5
- Add support for language change from boot loader via boot-i18n service

* Thu Jun 26 2008  Muayyad Saleh Alsadi <alsadi@ojuba.org> - 1.0.0-4
- Change default panel layout

* Fri Jun 20 2008  Muayyad Saleh Alsadi <alsadi@ojuba.org> - 1.0.0-3
- Add intel wireless hack to /etc/modprobe.d/
- Add ojuba icons theme

* Fri Jun 20 2008  Muayyad Saleh Alsadi <alsadi@ojuba.org> - 1.0.0-2
- Add bash history confs

* Thu Jun 12 2008 Muayyad Saleh Alsadi <alsadi@ojuba.org> - 1.0.0-1
- Initial version

