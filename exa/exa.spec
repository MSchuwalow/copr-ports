Name:           exa
Summary:        Replacement for 'ls' written in Rust. https://the.exa.website/
License:        MIT
Release:        1%{?dist}

%define git_owner       ogham
%define git_url         https://github.com/%{git_owner}/%{name}

URL:            %{git_url}

%define use_pinned      0
%define pinned          3d75c491912952d2a18fb34ab81221b1bded07d5
%if %{use_pinned} || %(command -v git > /dev/null; echo $?)
%define git_rev         %{pinned}
%else
%define git_rev         %(git ls-remote %{git_url} HEAD | cut -f 1)
%endif
%define abbrev          %(printf '%0.7s' %{git_rev})

Version:        git%(date '+%Y%m%d').%{abbrev}
Source0:        %{git_url}/tarball/%{git_rev}#/%{git_owner}-%{name}-%{abbrev}.tar.gz

Requires: libgit2

BuildRequires: git
BuildRequires: rust
BuildRequires: cargo

%description
exa is a replacement for ls written in Rust.

%prep
%setup -qn %{git_owner}-%{name}-%{abbrev}

%build
env CARGO_INCREMENTAL=0 cargo build --release

%install
install -D -m755 target/release/%{name} %{buildroot}/%{_bindir}/%{name}

%files
%{_bindir}/exa

%changelog
