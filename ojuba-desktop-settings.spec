Name:           ojuba-desktop-settings
Version:        16.0.5
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
Requires(posttrans): glib2 GConf2 systemd-units
BuildRequires: systemd-units
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
chmod +x $RPM_BUILD_ROOT/%{_bindir}/*
chmod +x $RPM_BUILD_ROOT/%{_sbindir}/*

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
gconftool-2 --direct --config-source=xml:readwrite:/etc/gconf/gconf.xml.defaults -s /apps/metacity/general/titlebar_font --type string 'Sans Bold 11' &> /dev/null || :
gconftool-2 --direct --config-source=xml:readwrite:/etc/gconf/gconf.xml.defaults \
            -s /apps/gnome-terminal/profiles/Default/use_theme_colors --type bool false &> /dev/null || :
gconftool-2 --direct --config-source=xml:readwrite:/etc/gconf/gconf.xml.defaults \
            -s /apps/gnome-terminal/profiles/Default/foreground_color --type string '#FFFFFF' &> /dev/null || :
gconftool-2 --direct --config-source=xml:readwrite:/etc/gconf/gconf.xml.defaults \
            -s /apps/gnome-terminal/profiles/Default/background_color --type string '#000000' &> /dev/null || :
            
gconftool-2 --direct --config-source=xml:readwrite:/etc/gconf/gconf.xml.defaults \
            -s /apps/gnome-terminal/profiles/Default/background_type --type string 'transparent' &> /dev/null || :
gconftool-2 --direct --config-source=xml:readwrite:/etc/gconf/gconf.xml.defaults \
            -s /apps/gnome-terminal/profiles/Default/background_darkness --type float 0.8 &> /dev/null || :
gconftool-2 --direct --config-source=xml:readwrite:/etc/gconf/gconf.xml.defaults \
            -s /apps/gnome-terminal/profiles/Default/use_custom_default_size --type bool true &> /dev/null || :
gconftool-2 --direct --config-source=xml:readwrite:/etc/gconf/gconf.xml.defaults \
            -s /apps/gnome-terminal/profiles/Default/default_size_rows --type int 24 &> /dev/null || :
gconftool-2 --direct --config-source=xml:readwrite:/etc/gconf/gconf.xml.defaults \
            -s /apps/gnome-terminal/profiles/Default/default_size_columns --type int 100 &> /dev/null || :

# Fix xkeyboard-config right alt bug, this is only needed when if we don't have that package
# sed -rie  '/ralt_switch/ s;(.*$);//\1;' /usr/share/X11/xkb/symbols/ara &> /dev/null || :

# enable SysRQ 
# fix initscripts bug rhbz #760254
sed -i '/kernel.sysrq/ s/=.*/= 1/' /etc/sysctl.conf &> /dev/null || : 
echo 1 > /proc/sys/kernel/sysrq &> /dev/null || :

if [ -x /bin/systemctl ];then
  # FIXME: is this needed ?
  # systemctl daemon-reload &> /dev/null || :
  systemctl enable ojuba-boot-params.service &> /dev/null || :
fi
# Setup bluetooth service as multi-user.target service
[ -e /etc/systemd/system/multi-user.target.wants/bluetooth.service ] || ln -s '/lib/systemd/system/bluetooth.service' '/etc/systemd/system/multi-user.target.wants/bluetooth.service'  &> /dev/null || :

%postun
if [ $1 -eq 0 ]; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi
gconftool-2 --direct --config-source=xml:readwrite:/etc/gconf/gconf.xml.defaults -s /apps/metacity/general/titlebar_font --type string 'Cantarell Bold 11' &> /dev/null || :

if [ -f /etc/systemd/system/multi-user.target.wants/ojuba-boot-params.service ];then
  /bin/rm -f /etc/systemd/system/multi-user.target.wants/ojuba-boot-params.service  &> /dev/null || :
fi

%files
%config(noreplace) /etc/X11/xorg.conf.d/00-touchpad.conf
%config(noreplace) /etc/X11/xinit/xinitrc.d/xim4arabic.sh
%config(noreplace) /etc/modprobe.d/*
%config(noreplace) /etc/profile.d/*
%config(noreplace) /etc/fonts/conf.d/*
%config(noreplace) /etc/fonts/conf.avail/*
%config(noreplace) /etc/skel/.mplayer/config
/etc/sysctl.d/*
%{_datadir}/glib-2.0/schemas/*.override
/var/lib/polkit-1/localauthority/10-vendor.d/*
%{_bindir}/*
%{_sbindir}/*
%{_unitdir}/*


%changelog
* Fri Mar 09 2012 Ehab El-Gedawy <ehabsas@gmail.com> - 16.0.3
- enable bluetooth
- accept some boot params like
  * xscreen=<WIDTH>x<HEIGHT>[x<DEPTH>] (eg. 800x600)
  * xdriver
  * lang

* Sat Dec 31 2011  Muayyad Saleh Alsadi <alsadi@ojuba.org> - 16.0.0-1
- add favorited apps
- add default extensions

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

