Name:           alacritty
Summary:        A cross-platform, GPU enhanced terminal emulator
License:        ASL 2.0
Release:        1%{?dist}

%define git_owner       jwilm
%define git_url         https://github.com/%{git_owner}/%{name}

URL:            %{git_url}

%define git_rev         1b7ffea136f55236729258ddbc6841282de91ae9
%define abbrev          %(printf '%0.7s' %{git_rev})

Version:        git%(date '+%Y%m%d').%{abbrev}
Source0:        %{git_url}/tarball/%{git_rev}#/%{git_owner}-%{name}-%{abbrev}.tar.gz

Requires: git
Requires: freetype
Requires: fontconfig
Requires: xclip

BuildRequires: freetype-devel
BuildRequires: fontconfig-devel
BuildRequires: xclip
BuildRequires: pkg-config
BuildRequires: cmake
BuildRequires: gcc-c++

# Check ~/.cargo/bin/* before going system-wide
%if %(command -v rustc &> /dev/null; echo $?)
BuildRequires:  rust
%endif
%if %(command -v cargo &> /dev/null; echo $?)
BuildRequires:  cargo
%endif


%description
Alacritty is the fastest terminal emulator in existence. Using the GPU for
rendering enables optimizations that simply aren't possible in other emulators.

%prep
%setup -qn %{git_owner}-%{name}-%{abbrev}

%build
env CARGO_INCREMENTAL=0 cargo build --release

%install
install -D -m755 target/release/%{name} %{buildroot}/%{_bindir}/%{name}
install -D -m644 Alacritty.desktop %{buildroot}/%{_datadir}/applications/Alacritty.desktop
install -d -m755 %{buildroot}/%{_datadir}/%{name}
install -m644 alacritty*.yml %{buildroot}/%{_datadir}/%{name}
install -d -m755 %{buildroot}/%{_datadir}/terminfo/a
tic -o %{buildroot}/%{_datadir}/terminfo alacritty.info

%post
update-desktop-database &> /dev/null ||:

%postun
update-desktop-database &> /dev/null ||:

%posttrans
desktop-file-validate %{_datadir}/applications/alacritty.desktop &> /dev/null || :

%files
%{_bindir}/alacritty
%{_datadir}/applications/*.desktop
%{_datadir}/%{name}/*.yml
%{_datadir}/terminfo/*

%changelog
* Mon Apr 16 2018 MSchuwalow <mschuwalow@uos.de> git20180416.1b7ffea-1
- switched to explicit hashes instead of autodiscovery for easier old builds
  (mschuwalow@uos.de)
- removed old alacritty sources (mschuwalow@uos.de)

