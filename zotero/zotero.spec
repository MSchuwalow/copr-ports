Name:           zotero
Summary:        Zotero is a free, easy-to-use tool to help you collect, organize, cite, and share your research sources. https://www.zotero.org
License:        GNU AGPLv3

Version:		5.0.44
Release:        2%{?dist}

URL:            https://www.zotero.org

Source0:        https://download.zotero.org/client/release/%{version}/Zotero-%{version}_linux-x86_64.tar.bz2

%description
Zotero is a free, easy-to-use tool to help you collect, organize, cite, and share your research sources.

%define source_dir Zotero_linux-x86_64

%prep
%setup -cn %{source_dir} 
# Disable APP update
sed -i '/pref("app.update.enabled", true);/c\pref("app.update.enabled", false);' %{source_dir}/defaults/preferences/prefs.js
sed -i "s/zotero.ico/zotero.png/" %{source_dir}/zotero.desktop

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_datadir}/applications
mkdir -p %{buildroot}/usr/lib

cp -r %{source_dir}/ %{buildroot}/usr/lib/zotero

ln -s ../../usr/lib/%{name}/%{name} %{buildroot}/%{_bindir}/%{name}
ln -s ../../../usr/lib/%{name}/%{name}.desktop %{buildroot}/usr/share/applications/zotero.desktop

install -Dm644 %{source_dir}/chrome/icons/default/default16.png %{buildroot}/usr/share/icons/hicolor/16x16/apps/zotero.png
install -Dm644 %{source_dir}/chrome/icons/default/default32.png %{buildroot}/usr/share/icons/hicolor/32x32/apps/zotero.png
install -Dm644 %{source_dir}/chrome/icons/default/default48.png %{buildroot}/usr/share/icons/hicolor/48x48/apps/zotero.png
install -Dm644 %{source_dir}/chrome/icons/default/default256.png %{buildroot}/usr/share/icons/hicolor/256x256/apps/zotero.png

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database &> /dev/null ||:

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database &> /dev/null ||:

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
desktop-file-validate %{_datadir}/applications/%{name}.desktop &> /dev/null || :

%files
%{_bindir}/%{name}
/usr/lib/%{name}
%{_datadir}/applications/*.desktop
/usr/share/icons/hicolor/16x16/apps/zotero.png
/usr/share/icons/hicolor/32x32/apps/zotero.png
/usr/share/icons/hicolor/48x48/apps/zotero.png
/usr/share/icons/hicolor/256x256/apps/zotero.png

%changelog
* Wed Apr 11 2018 Maxim Schuwalow <mschuwalow@uos.de> 5.0.44-2
- updated project configuration

