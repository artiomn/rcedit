{
  'variables': {
    'conditions': [
      ['OS=="win" and (MSVS_VERSION=="2012e" or MSVS_VERSION=="2010e")', {
        'msvs_express': 1,
        'windows_driver_kit_path%': 'C:/WinDDK/7600.16385.1',
      },{
        'msvs_express': 0,
      }],
      ['OS=="win" and (MSVS_VERSION =="2012e" or MSVS_VERSION=="2012")', {
        'msbuild_toolset': 'v110_xp',
      }],
      ['OS=="win" and (MSVS_VERSION=="2013e" or MSVS_VERSION=="2013")', {
        'msbuild_toolset': 'v120_xp',
      }],
      ['OS=="win" and (MSVS_VERSION=="2015")', {
        'msbuild_toolset': 'v140_xp',
      }],
      ['OS=="win" and (MSVS_VERSION=="2017")', {
        'msbuild_toolset': 'v141_xp',
      }],
    ],
  },
  'targets': [
    {
      'target_name': 'rcedit',
      'type': 'executable',
      'sources': [
        'src/main.cc',
        'src/rescle.cc',
        'src/rescle.h',
        'src/rcedit.rc',
      ],
      'msvs_settings': {
        'VCLinkerTool': {
          'SubSystem': 1, # console executable
        },
        'VCCLCompilerTool': {
          'Optimization': 3, # /Ox, full optimization
          'FavorSizeOrSpeed': 1, # /Os, favour small code
          'RuntimeLibrary': 0, # /MT, for statically linked runtime
        },
      },
      'conditions': [
        ['OS=="win" and "<(msbuild_toolset)"!=""', {
          'msbuild_toolset': '<(msbuild_toolset)',
        }],
        # Using Visual Studio Express.
        ['msvs_express==1', {
          'defines!': [
            '_SECURE_ATL',
          ],
          'msvs_settings': {
            'VCLibrarianTool': {
              'AdditionalLibraryDirectories': [
                '<(windows_driver_kit_path)/lib/ATL/i386',
              ],
            },
            'VCLinkerTool': {
              'AdditionalLibraryDirectories': [
                '<(windows_driver_kit_path)/lib/ATL/i386',
              ],
              'AdditionalDependencies': [
                'atlthunk.lib',
              ],
              'AdditionalOptions': [
                # ATL 8.0 included in WDK 7.1 makes the linker to generate following
                # warnings:
                #   - warning LNK4254: section 'ATL' (50000040) merged into
                #     '.rdata' (40000040) with different attributes
                #   - warning LNK4078: multiple 'ATL' sections found with
                #     different attributes
                '/ignore:4254',
                '/ignore:4078',
              ],
            },
          },
          'msvs_system_include_dirs': [
            '<(windows_driver_kit_path)/inc/atl71',
            '<(windows_driver_kit_path)/inc/mfc42',
          ],
        }],  # msvs_express==1
      ],
    },
  ],
}
