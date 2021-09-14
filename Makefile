SHELL=/bin/sh
APPNAME=ojuba-desktop-settings
DESTDIR?=/
DATADIR=$(DESTDIR)/usr/
SYSCONFDIR=$(DESTDIR)/etc/


ECHO := echo
INSTALL := install
RM := $(shell which rm | egrep '/' | sed  's/\s//g')

install all:  einstall install-fonts-conf install-polkit-rules install-bash-profile install-glib-schemas
	
einstall:
	@$(ECHO) "*** Installing $(APPNAME)..."
	@for i in "background-transparency-percent 20" "cursor-shape 'underline'" "default-size-columns 118" "default-size-rows 25" "title-mode 'ignore'" "use-transparent-background true"; do \
		dconf write /org/gnome/terminal/legacy/profiles:/:$$(dconf read /org/gnome/terminal/legacy/profiles:/default|sed s/\'//g)/$${i} ;\
	done

install-fonts-conf: einstall
	@$(ECHO) "+ Installing font config..."
	@$(INSTALL) -d $(SYSCONFDIR)/fonts/{conf.avail,conf.d}/
	@for i in ./etc/fonts/conf.avail/*; do \
		$(ECHO) "    -- Installing $${i/./}..."; \
		$(INSTALL) -m 0644 $${i} $(SYSCONFDIR)/fonts/conf.avail/; \
	done
	@for i in ./etc/fonts/conf.d/*; do \
	    $(ECHO) "    -- Installing $${i/./}..."; \
	    $(INSTALL) -m 0644 $${i} $(SYSCONFDIR)/fonts/conf.d/; \
	done
	
install-polkit-rules: einstall
	@$(ECHO) "+ Installing PolicyKit rules..."
	@$(INSTALL) -d $(SYSCONFDIR)/polkit-1/rules.d/
	@for i in ./etc/polkit-1/rules.d/*; do \
		$(ECHO) "    -- Installing $${i/./}..."; \
		$(INSTALL) -m 0644 $${i} $(SYSCONFDIR)/polkit-1/rules.d/; \
	done
	
install-bash-profile: einstall
	@$(ECHO) "+ Installing Bash profile..."
	@$(INSTALL) -d $(SYSCONFDIR)/profile.d/
	@for i in ./etc/profile.d/*; do \
		$(ECHO) "    -- Installing $${i/./}..."; \
		$(INSTALL) -m 0644 $${i} $(SYSCONFDIR)/profile.d/; \
	done
	
install-glib-schemas: einstall
	@$(ECHO) "+ Installing Glib override schemas..."
	@$(INSTALL) -d $(DATADIR)/share/glib-2.0/schemas/
	@for i in ./usr/share/glib-2.0/schemas/*; do \
		$(ECHO) "    -- Installing $${i/./}..."; \
		$(INSTALL) -m 0644 $${i} $(DATADIR)/share/glib-2.0/schemas/; \
	done
	@if [ $(DESTDIR) == "/" ] ; then \
	    @glib-compile-schemas $(DATADIR)/../usr/share/glib-2.0/schemas/ &> /dev/null || : ;\
	fi
	
uninstall: euninstall uninstall-font-conf uninstall-polkit-rules uninstall-bash-profile uninstall-glib-schemas
	
	
euninstall: 
	@$(ECHO) "*** Uninstalling $(APPNAME)... "
	@dconf reset -f /org/gnome/terminal/legacy/profiles:/:$$(dconf read /org/gnome/terminal/legacy/profiles:/default|sed s/\'//g)/
	
uninstall-font-conf: euninstall
	@$(ECHO) "- Removing: font config."
	@for i in ./etc/fonts/conf.avail/*; do \
		$(ECHO) "    -- Unnstalling $${i/./}..."; \
		$(RM) -f $(SYSCONFDIR)/../$${i}; \
	done
	@for i in ./etc/fonts/conf.d/*; do \
	    $(ECHO) "    -- Uninstalling $${i/./}..."; \
	    $(RM) -f $(SYSCONFDIR)/../$${i}; \
	done

uninstall-polkit-rules: euninstall
	@$(ECHO) "- Removing: PolicyKit rules."
	@for i in ./etc/polkit-1/rules.d/*; do \
		$(ECHO) "    -- Unnstalling $${i/./}..."; \
		$(RM) -f $(SYSCONFDIR)/../$${i}; \
	done

uninstall-bash-profile: euninstall
	@$(ECHO) "- Removing: Bash profile."
	@for i in ./etc/profile.d/*; do \
		$(ECHO) "    -- Unnstalling $${i/./}..."; \
		$(RM) -f $(SYSCONFDIR)/../$${i}; \
	done
	
uninstall-glib-schemas: euninstall
	@$(ECHO) "- Removing: Glib override schemas."
	@for i in ./usr/share/glib-2.0/schemas/*; do \
		$(ECHO) "    -- Unnstalling $${i/./}..."; \
		$(RM) -f $(DATADIR)/../$${i}; \
	done
	@if [ $(DESTDIR) == "/" ] ; then \
	    @glib-compile-schemas $(DATADIR)/../usr/share/glib-2.0/schemas/ &> /dev/null || : ;\
	fi
	
