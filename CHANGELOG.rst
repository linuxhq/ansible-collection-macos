===========================
linuxhq.macos Release Notes
===========================

.. contents:: Topics

v1.1.3
======

Release Summary
---------------

Splits the homebrew role into dedicated formulae, cask, and tap roles, adds Homebrew and launchd info modules and roles, brings Tart-based molecule scenarios to every role, removes the delisted hermes role, and raises the minimum supported ansible-core to 2.18.0.

Minor Changes
-------------

- adguard, appzapper, iterm2, monitorcontrol, proton_drive, proton_mail, proton_vpn, rectangle, sizeup, textual - support uninstalling the cask via a new ``{role}_state`` variable, and removing individual defaults entries via a per-item ``state`` key; both default to ``present``.
- homebrew_tap - trust taps with ``brew trust`` after tapping so packages from third-party taps can be installed.
- irssi - support uninstalling the package and removing the configuration directory via a new ``irssi_state`` variable, defaulting to ``present``.
- liquidprompt - support uninstalling the package and removing the configuration via a new ``liquidprompt_state`` variable, defaulting to ``present``.
- meta - exclude development, CI, and tooling files from the built collection tarball via ``build_ignore``.
- meta - remove the deprecated ``ansible_managed`` comment header from all role templates.
- meta - require community.general 13.2.0 or later.
- privoxy - default ``privoxy_templdir``, ``privoxy_temporary_directory``, and ``privoxy_trustfile`` to ``null`` instead of an empty string, matching the collection's convention for unset string variables; existing empty-string overrides are still treated as unset.
- privoxy - start the service after the configuration is managed; when ``privoxy_state`` is ``absent`` the service is stopped before the package is uninstalled, the configuration file is removed, and the restart handler is skipped.
- privoxy - support uninstalling the package via a new ``privoxy_state`` variable, defaulting to ``present``.
- rclone - gather launchd agent status with the ``launchd_info`` module and only start agents that are not already running.
- rclone - manage the launchd agents with the ``community.general.launchd`` module instead of a raw ``launchctl load`` command; agents are now reloaded when their property list changes and report idempotent results.
- rclone - mount remotes with ``rclone nfsmount`` instead of ``rclone mount``, removing the macFUSE requirement on macOS.
- rclone - only create the ``~/Library/LaunchAgents`` directory when mounts are defined.
- rclone - update the default rclone version to v1.74.4.
- shell_proxy - support removing the proxy file via a new ``shell_proxy_state`` variable, defaulting to ``present``.

Breaking Changes / Porting Guide
--------------------------------

- homebrew - move cask management to the new ``homebrew_cask`` role; the ``homebrew_casks``, ``homebrew_sudo_password``, and ``homebrew_upgrade_greedy`` variables are removed.
- homebrew - move tap management to the new ``homebrew_tap`` role; the ``homebrew_taps`` variable is removed.
- homebrew - rename the ``homebrew_packages`` variable to ``homebrew_list``.
- meta - raise the minimum supported ansible-core version to 2.18.0 across the collection and every role; upgrade ansible-core on the control node to 2.18.0 or later before installing this release.
- rclone - install the package with Homebrew instead of downloading release archives from downloads.rclone.org; the ``rclone_version`` variable is removed and ``rclone_path_bin`` is now a list of directories searched for the binary via the launchd agent's ``PATH``.
- rclone - remove the ``rclone_path_plist`` variable; agent property lists are always written to ``~/Library/LaunchAgents``, the only user-writable location the ``community.general.launchd`` module searches.

Removed Features (previously deprecated)
----------------------------------------

- hermes - remove the role; the ``hermes`` cask was delisted from Homebrew after the application was abandoned upstream.

Bugfixes
--------

- irssi - close each chatnet block after all of its settings when rendering the configuration; previously a chatnet with more than one setting leaked the extra settings outside its block.
- irssi - sort channels, ignores, and servers by their identifying key when rendering the configuration; previously the template failed with a ``TypeError`` as soon as any of these lists held more than one entry.
- irssi, liquidprompt, shell_proxy - resolve the default destination paths from the target host's ``HOME`` via gathered facts instead of the control node's environment, so remote hosts are no longer configured with the controller's home directory.
- privoxy - restart the service with the ``community.general.homebrew_services`` module instead of a raw ``brew services restart`` command, so the restart handler reports its change in the play recap.
- privoxy - support check mode on hosts where the package is not yet installed; the service tasks and restart handler no longer fail probing a missing formula during a dry run.
- rclone - escape XML special characters when rendering launchd property list files; mount names, remotes, mountpoints, and flags containing characters such as ``&`` previously produced an invalid plist.
- rclone - preserve float values in the rendered configuration; previously options such as a ``tpslimit`` of ``0.5`` were truncated to integers.
- rclone - translate the ``x86_64`` architecture fact to rclone's ``amd64`` release naming; previously the download URL returned a 404 on Intel Macs.
- shell_proxy - URL-encode proxy usernames and passwords so credentials containing characters such as ``@`` or ``:`` no longer corrupt the exported proxy URLs.

New Modules
-----------

- homebrew_cask_info - Gather information about Homebrew casks.
- homebrew_info - Gather information about Homebrew formulae.
- homebrew_services_info - Gather information about Homebrew services.
- launchd_info - Gather information about launchd services.

New Roles
---------

- homebrew_cask - Manage homebrew casks.
- homebrew_cask_info - Gather information about Homebrew casks.
- homebrew_info - Gather information about Homebrew formulae.
- homebrew_services_info - Gather information about Homebrew services.
- homebrew_tap - Manage homebrew taps.
- launchd_info - Gather information about launchd services.

v1.1.2
======

Release Summary
---------------

Updates the default rclone version to v1.73.0, which adds support for the Drime and Filen backends.

Minor Changes
-------------

- rclone - update the default rclone version to v1.73.0.

v1.1.1
======

Release Summary
---------------

Adds a new homebrew role for managing casks, packages, and taps.

Minor Changes
-------------

- homebrew - initial commit.

v1.1.0
======

Release Summary
---------------

First release with the changelog included.

Minor Changes
-------------

- meta - update copyrights in readme and meta files.
- rclone - convert rclone_conf from a dict to a list.
