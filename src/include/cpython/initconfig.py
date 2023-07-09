__all__ = [
    'PyStatus', 'PyStatus_p',
    'PyWideStringList', 'PyWideStringList_p',
    'PyPreConfig', 'PyPreConfig_p',
    'PyConfig', 'PyConfig_p',
]


import ctypes

from ... import PyAPI_FUNC


### --- PyStatus -----------------------------------------------


class PyStatus(ctypes.Structure):
    """
    enum {
        _PyStatus_TYPE_OK=0,
        _PyStatus_TYPE_ERROR=1,
        _PyStatus_TYPE_EXIT=2
    } _type;
    const char *func;
    const char *err_msg;
    int exitcode;
    """

    _fields_ = [
        ('_type'    , ctypes.c_int    ),
        ('func'     , ctypes.c_char_p ),
        ('err_msg'  , ctypes.c_char_p ),
        ('exitcode' , ctypes.c_int    ),
    ]


PyStatus_p = ctypes.POINTER(PyStatus)


###


PyAPI_FUNC("PyStatus_Ok",
    restype = PyStatus,
    )

PyAPI_FUNC("PyStatus_Error",
    restype = PyStatus,
    argtypes = [
        ctypes.c_char_p,
    ])

PyAPI_FUNC("PyStatus_NoMemory",
    restype = PyStatus,
    )

PyAPI_FUNC("PyStatus_Exit",
    restype = PyStatus,
    argtypes = [
        ctypes.c_int,
    ])

PyAPI_FUNC("PyStatus_IsError",
    restype = ctypes.c_int,
    argtypes = [
        PyStatus,
    ])

PyAPI_FUNC("PyStatus_IsExit",
    restype = ctypes.c_int,
    argtypes = [
        PyStatus,
    ])

PyAPI_FUNC("PyStatus_Exception",
    restype = ctypes.c_int,
    argtypes = [
        PyStatus,
    ])


### --- PyWideStringList ------------------------------------------------


class PyWideStringList(ctypes.Structure):
    """
    Py_ssize_t length;
    wchar_t **items;
    """

    # If length is greater than zero, items must be non-NULL
    # and all items strings must be non-NULL

    _fields_ = [
        ('length' , ctypes.py_ssize_t ),
        ('items'  , ctypes.c_wchar_pp ),
    ]


PyWideStringList_p = ctypes.POINTER(PyWideStringList)


###


PyAPI_FUNC("PyWideStringList_Append",
    restype = PyStatus,
    argtypes = [
        PyWideStringList_p,
        ctypes.c_wchar_p,
    ])

PyAPI_FUNC("PyWideStringList_Insert",
    restype = PyStatus,
    argtypes = [
        PyWideStringList_p,
        ctypes.py_ssize_t,
        ctypes.c_wchar_p,
    ])


### --- PyPreConfig -----------------------------------------------


class PyPreConfig(ctypes.Structure):
    """
    int _config_init;
    int parse_argv;
    int isolated;
    int use_environment;
    int configure_locale;
    int coerce_c_locale;
    int coerce_c_locale_warn;
#ifdef MS_WINDOWS
    int legacy_windows_fs_encoding;
#endif
    int utf8_mode;
    int dev_mode;
    int allocator;
    """

    _fields_ = [
        # `_PyConfigInitEnum` value
        ('_config_init'                    , ctypes.c_int ),

        # Parse Py_PreInitializeFromBytesArgs() arguments?
        # - See `PyConfig.parse_argv`
        ('parse_argv'                      , ctypes.c_int ),

        # - If set to -1 (default), inherit `Py_IsolatedFlag` value.
        # - If greater than 0, enable isolated mode: `sys.path` contains
        #   neither the script's directory nor the user's `site-packages`
        #   directory.
        # - Set to 1 by the `-I` command line option.
        ('isolated'                        , ctypes.c_int ),

        # - If set to -1 (default), it is set to `!Py_IgnoreEnvironmentFlag`.
        # - If greater than 0: use environment variables.
        # - Set to 0 by `-E` command line option.
        ('use_environment'                 , ctypes.c_int ),

        # Set the `LC_CTYPE` locale to the user preferred locale?
        # - If == 0, set `coerce_c_locale` and `coerce_c_locale_warn` to 0.
        ('configure_locale'                , ctypes.c_int ),

        # Coerce the `LC_CTYPE` locale if it's equal to "C"? (PEP 538)
        # - Disable by default (set to 0).
        # - Set to 0 by `PYTHONCOERCECLOCALE=0`.
        # - Set to 1 by `PYTHONCOERCECLOCALE=1`.
        # - Set to 2 if the user preferred `LC_CTYPE` locale is "C".
        # - Set it to -1 to let Python decide if it should be enabled or not.
        # - If it is equal to 1, `LC_CTYPE` locale is read to decide if it
        #   should be coerced or not (ex: `PYTHONCOERCECLOCALE=1`).
        # - Internally, it is set to 2 if `LC_CTYPE` locale must be coerced.
        ('coerce_c_locale'                 , ctypes.c_int ),

        # Emit a warning if the `LC_CTYPE` locale is coerced?
        # - Disable by default (set to 0).
        # - Set to 1 by `PYTHONCOERCECLOCALE=warn`.
        # - Set it to -1 to let Python decide if it should be enabled or not.
        ('coerce_c_locale_warn'            , ctypes.c_int ),

        # - If set to -1 (default), inherit `Py_LegacyWindowsFSEncodingFlag`
        # - If greater than 1, use the "mbcs" encoding instead of the UTF-8
        #   encoding for the filesystem encoding.
        # - Set to 1 if the `PYTHONLEGACYWINDOWSFSENCODING` environment
        #   variable is set to a non-empty string.
        # - See PEP 529 for more details.
        *(
            (('legacy_windows_fs_encoding' , ctypes.c_int ),
             )
            if ctypes.pyconfig.MS_WINDOWS
            else ()
        ),

        # Enable UTF-8 mode? (PEP 540)
        # - Disabled by default (equals to 0).
        # - If equals to -1, it is set to 1 if the `LC_CTYPE` locale
        #   is "C" or "POSIX", otherwise it is set to 0.
        # - Inherit `Py_UTF8Mode` value value.
        # - Set to 0 by "-X utf8=0" and `PYTHONUTF8=0`
        # - Set to 1 by "-X utf8" and "-X utf8=1" command line options.
        # - Set to 1 by `PYTHONUTF8=1` environment variable.
        ('utf8_mode'                       , ctypes.c_int ),

        # - If non-zero, enable the Python Development Mode.
        # - Set to 1 by the `-X` dev command line option.
        # - Set by the `PYTHONDEVMODE` environment variable.
        ('dev_mode'                        , ctypes.c_int ),

        # Memory allocator: `PYTHONMALLOC` env var.
        # - See `PyMemAllocatorName` for valid values.
        ('allocator'                       , ctypes.c_int ),
    ]



PyPreConfig_p = ctypes.POINTER(PyPreConfig)


###


PyAPI_FUNC("PyPreConfig_InitPythonConfig",
    argtypes = [
        PyPreConfig_p,
    ])

PyAPI_FUNC("PyPreConfig_InitIsolatedConfig",
    argtypes = [
        PyPreConfig_p,
    ])


### --- PyConfig ----------------------------------------------


class PyConfig(ctypes.Structure):
    """
    int _config_init;
    int isolated;
    int use_environment;
    int dev_mode;
    int install_signal_handlers;
    int use_hash_seed;
    unsigned long hash_seed;
    int faulthandler;
    int _use_peg_parser;
    int tracemalloc;
    int import_time;
    int show_ref_count;
    int dump_refs;
    int malloc_stats;
    wchar_t *filesystem_encoding;
    wchar_t *filesystem_errors;
    wchar_t *pycache_prefix;
    int parse_argv;
    PyWideStringList argv;
    wchar_t *program_name;
    PyWideStringList xoptions;
    PyWideStringList warnoptions;
    int site_import;
    int bytes_warning;
    int inspect;
    int interactive;
    int optimization_level;
    int parser_debug;
    int write_bytecode;
    int verbose;
    int quiet;
    int user_site_directory;
    int configure_c_stdio;
    int buffered_stdio;
    wchar_t *stdio_encoding;
    wchar_t *stdio_errors;
#ifdef MS_WINDOWS
    int legacy_windows_stdio;
#endif
    wchar_t *check_hash_pycs_mode;
    int pathconfig_warnings;
    wchar_t *pythonpath_env;
    wchar_t *home;
    int module_search_paths_set;
    PyWideStringList module_search_paths;
    wchar_t *executable;
    wchar_t *base_executable;
    wchar_t *prefix;
    wchar_t *base_prefix;
    wchar_t *exec_prefix;
    wchar_t *base_exec_prefix;
    wchar_t *platlibdir;
    int skip_source_first_line;
    wchar_t *run_command;
    wchar_t *run_module;
    wchar_t *run_filename;
    int _install_importlib;
    int _init_main;
    int _isolated_interpreter;
    PyWideStringList _orig_argv;
    """

    _fields_ = [
        # `_PyConfigInitEnum` value
        ('_config_init'              , ctypes.c_int     ),

        # Isolated mode?
        # - See `PyPreConfig.isolated`
        ('isolated'                  , ctypes.c_int     ),

        # Use environment variables?
        # - See `PyPreConfig.use_environment`
        ('use_environment'           , ctypes.c_int     ),

        # Python Development Mode?
        # - See `PyPreConfig.dev_mode`
        ('dev_mode'                  , ctypes.c_int     ),

        # Install signal handlers?
        # - Yes by default.
        ('install_signal_handlers'   , ctypes.c_int     ),

        # `PYTHONHASHSEED=x`
        ('use_hash_seed'             , ctypes.c_int     ),
        ('hash_seed'                 , ctypes.c_ulong   ),

        # Enable faulthandler?
        # - Value of -1 means unset.
        # - Set to 1 by `-X` faulthandler and PYTHONFAULTHANDLER.
        ('faulthandler'              , ctypes.c_int     ),

        # Enable PEG parser?
        # - Set to 0 by `-X` oldparser and `PYTHONOLDPARSER`
        # - Set to 1 by default
        ('_use_peg_parser'           , ctypes.c_int     ),

        # Enable tracemalloc?
        # - Value of -1 means unset
        # - Set by `-X` tracemalloc=N and `PYTHONTRACEMALLOC`.
        ('tracemalloc'               , ctypes.c_int     ),

        # `PYTHONPROFILEIMPORTTIME`, `-X` importtime
        ('import_time'               , ctypes.c_int     ),

        # `-X` showrefcount
        ('show_ref_count'            , ctypes.c_int     ),

        # `PYTHONDUMPREFS`
        ('dump_refs'                 , ctypes.c_int     ),

        # `PYTHONMALLOCSTATS`
        ('malloc_stats'              , ctypes.c_int     ),

        # Python filesystem encoding and error handler:
        # - Default encoding and error handler:
        #   - if `Py_SetStandardStreamEncoding()` has been called:
        #     they have the highest priority;
        #   - `PYTHONIOENCODING` environment variable;
        #   - The UTF-8 Mode uses UTF-8/surrogateescape;
        #   - If Python forces the usage of the ASCII encoding (ex: C locale
        #     or POSIX locale on FreeBSD or HP-UX), use ASCII/surrogateescape;
        #   - locale encoding: ANSI code page on Windows, UTF-8 on Android and
        #     VxWorks, `LC_CTYPE` locale encoding on other platforms;
        #   - On Windows, "surrogateescape" error handler;
        #   - "surrogateescape" error handler if the `LC_CTYPE` locale
        #     is "C" or "POSIX";
        #   - "surrogateescape" error handler if the `LC_CTYPE` locale
        #     has been coerced (PEP 538);
        #   - "strict" error handler.
        # - Supported error handlers: "strict", "surrogateescape" and
        #   "surrogatepass". The surrogatepass error handler is only supported
        #   if `Py_DecodeLocale()` and `Py_EncodeLocale()` use directly the
        #   UTF-8 codec; it's only used on Windows.
        # - On Windows, sys._enablelegacywindowsfsencoding() sets the
        #   encoding/errors to mbcs/replace at runtime.

        # `sys.getfilesystemencoding()`
        ('filesystem_encoding'       , ctypes.c_wchar_p ),

        # `sys.getfilesystemencodeerrors()`
        ('filesystem_errors'         , ctypes.c_wchar_p ),

        # `PYTHONPYCACHEPREFIX`, `-X` pycache_prefix=PATH
        ('pycache_prefix'            , ctypes.c_wchar_p ),

        # Parse argv command line arguments?
        ('parse_argv'                , ctypes.c_int     ),

        # Command line arguments (`sys.argv`).
        # - Set `parse_argv` to 1 to `parse argv` as Python command line
        #   arguments and then strip Python arguments from `argv`.
        # - If `argv` is empty, an empty string is added to ensure
        #   that `sys.argv` always exists and is never empty.
        ('argv'                      , PyWideStringList ),

        # Program name:
        # - If `Py_SetProgramName()` was called, use its value.
        # - On macOS, use `PYTHONEXECUTABLE` environment variable if set.
        # - If `WITH_NEXT_FRAMEWORK` macro is defined, use
        #   `__PYVENV_LAUNCHER__` environment variable is set.
        # - Use `argv[0]`` if available and non-empty.
        # - Use "python" on Windows, or "python3" on other platforms.
        ('program_name'              , ctypes.c_wchar_p ),

        # Command line `-X` options
        ('xoptions'                  , PyWideStringList ),

        # Warnings options: lowest to highest priority.
        # warnings.filters is built in the reverse order (high->low priority).
        ('warnoptions'               , PyWideStringList ),

        # - If set to -1 (default), it is set to `!Py_NoSiteFlag`.
        # - If equal to zero, disable the import of the module `site` and the
        #   `site`-dependent manipulations of `sys.path` that it entails.
        #   Also disable these manipulations if `site` is explicitly imported
        #   later (call `site.main()` if you want them to be triggered).
        # - Set to 0 by the `-S` command line option.
        ('site_import'               , ctypes.c_int     ),

        # Bytes warnings:
        # - If set to -1 (default), inherit `Py_BytesWarningFlag` value.
        # - If equal to 1, issue a warning when comparing `bytes` or
        #   `bytearray` with `str` or `bytes` with `int`.
        # - If equal or greater to 2, issue an error.
        # - Incremented by the `-b` command line option.
        ('bytes_warning'             , ctypes.c_int     ),

        # - If set to -1 (default), inherit `Py_InspectFlag` value.
        # - If greater than 0, enable inspect:
        #   When a script is passed as first argument or the `-c` option is
        #   used, enter interactive mode after executing the script or the
        #   command, even when `sys.stdin` does not appear to be a terminal.
        # - Incremented by the `-i` command line option.
        # - Set to 1 if the `PYTHONINSPECT` environment variable is non-empty.
        ('inspect'                   , ctypes.c_int     ),

        # - If set to -1 (default), inherit `Py_InteractiveFlag` value.
        # - If greater than 0: enable the interactive mode (REPL).
        # - Incremented by the `-i` command line option.
        ('interactive'               , ctypes.c_int     ),

        # Optimization level.
        # - If set to -1 (default), inherit `Py_OptimizeFlag` value.
        # - Incremented by the `-O` command line option.
        # - Set by the `PYTHONOPTIMIZE` environment variable.
        ('optimization_level'        , ctypes.c_int     ),

        # - If set to -1 (default), inherit `Py_DebugFlag` value.
        # - If greater than 0, enable the debug mode: turn on parser debugging
        #   output (for expert only, depending on compilation options).
        # - Incremented by the `-d` command line option.
        # - Set by the `PYTHONDEBUG` environment variable.
        ('parser_debug'              , ctypes.c_int     ),

        # - If set to -1 (default), it is set to `!Py_DontWriteBytecodeFlag`.
        # - If equal to 0, Python won't try to write ".pyc" files on the
        #   import of source modules.
        # - Set to 0 by the `-B` command line option,
        #   and the `PYTHONDONTWRITEBYTECODE` environment variable.
        ('write_bytecode'            , ctypes.c_int     ),

        # - If set to -1 (default), inherit `Py_VerboseFlag` value.
        # - If greater than 0, enable the verbose mode:
        #   Print a message, each time a module is initialized,
        #   showing the place (filename or built-in module) from which
        #   it is loaded.
        # - If greater or equal to 2:
        #   Print a message for each file that is checked for when searching
        #   for a module. Also provides information on module cleanup at exit.
        # - Incremented by the `-v` option.
        # - Set by the `PYTHONVERBOSE` environment variable.
        ('verbose'                   , ctypes.c_int     ),

        # - If set to -1 (default), inherit `Py_QuietFlag` value.
        # - If greater than 0, enable the quiet mode:
        #   Don't display the copyright and version messages,
        #   even in interactive mode.
        # - Incremented by the `-q` option.
        ('quiet'                     , ctypes.c_int     ),

        # - If set to -1 (default), it is set to `!Py_NoUserSiteDirectory`.
        # - If greater than 0, don't add the user `site-packages` directory
        #   to `sys.path`.
        # - Set to 0 by the `-s` and `-I` command line options , and the
        #   `PYTHONNOUSERSITE` environment variable.
        ('user_site_directory'       , ctypes.c_int     ),

        # - If non-zero,
        #   configure C standard steams (`stdio`, `stdout`, `stderr`):
        # - Set `O_BINARY` mode on Windows.
        # - If `buffered_stdio` is equal to zero, make streams unbuffered.
        #   Otherwise, enable streams buffering if interactive is non-zero.
        ('configure_c_stdio'         , ctypes.c_int     ),

        # - If set to -1 (default), it is set to `!Py_UnbufferedStdioFlag`.
        # - If equal to 0, enable unbuffered mode:
        #   Force the `stdout` and `stderr` streams to be unbuffered.
        # - Set to 0 by the `-u` option.
        # - Set by the `PYTHONUNBUFFERED` environment variable.
        ('buffered_stdio'            , ctypes.c_int     ),

        # Encoding of `sys.stdin`, `sys.stdout` and `sys.stderr`.
        # - Value set from `PYTHONIOENCODING` environment variable,
        #   and `Py_SetStandardStreamEncoding()` function.
        # - See also `stdio_errors` attribute.
        ('stdio_encoding'            , ctypes.c_wchar_p ),

        # Error handler of `sys.stdin` and `sys.stdout`.
        # - Value set from `PYTHONIOENCODING` environment variable and
        #   `Py_SetStandardStreamEncoding()` function.
        # - See also `stdio_encoding` attribute.
        ('stdio_errors'              , ctypes.c_wchar_p ),

        # - If set to -1 (default), inherit `Py_LegacyWindowsStdioFlag` value.
        # - If greater than 0, use `io.FileIO` instead of `WindowsConsoleIO`
        #   for `sys` standard streams.
        # - Set to 1 if the `PYTHONLEGACYWINDOWSSTDIO` environment variable
        #   is set to a non-empty string.
        # - See PEP 528 for more details.
        *(
            (('legacy_windows_stdio' , ctypes.c_int     ),
             )
            if ctypes.pyconfig.MS_WINDOWS
            else ()
        ),

        # Value of the `--check-hash-based-pycs` command line option:
        #   - "default" means the `check_source` flag in hash-based pycs
        #     determines invalidation
        #   - "always" causes the interpreter to hash the source file for
        #     invalidation regardless of value of `check_source` bit
        #   - "never" causes the interpreter to always assume hash-based pycs
        #     are valid
        #   - The default value is "default".
        # - See PEP 552 "Deterministic pycs" for more details.
        ('check_hash_pycs_mode'      , ctypes.c_wchar_p ),

        # --- Path configuration inputs ------------

        # - If set to -1 (default), inherit `!Py_FrozenFlag` value.
        # - If greater than 0:
        #   Suppress `_PyPathConfig_Calculate()` warnings on Unix.
        #   The parameter has no effect on Windows.
        ('pathconfig_warnings'       , ctypes.c_int     ),

        # `PYTHONPATH` environment variable
        ('pythonpath_env'            , ctypes.c_wchar_p ),

        # `PYTHONHOME` environment variable, see also `Py_SetPythonHome()`.
        ('home'                      , ctypes.c_wchar_p ),

        # --- Path configuration outputs -----------

        # - If non-zero, use `module_search_paths`
        ('module_search_paths_set'   , ctypes.c_int     ),

        # `sys.path` paths.
        # - Computed if `module_search_paths_set` is equal to 0.
        ('module_search_paths'       , PyWideStringList ),

        # `sys.executable`
        ('executable'                , ctypes.c_wchar_p ),

        # `sys._base_executable`
        ('base_executable'           , ctypes.c_wchar_p ),

        # `sys.prefix`
        ('prefix'                    , ctypes.c_wchar_p ),

        # `sys.base_prefix`
        ('base_prefix'               , ctypes.c_wchar_p ),

        # `sys.exec_prefix`
        ('exec_prefix'               , ctypes.c_wchar_p ),

        # `sys.base_exec_prefix`
        ('base_exec_prefix'          , ctypes.c_wchar_p ),

        # `sys.platlibdir`
        ('platlibdir'                , ctypes.c_wchar_p ),

        # --- Parameter only used by Py_Main() ----------

        # - Set by the `-x` command line option.
        # - Skip the first line of the source (`run_filename` parameter),
        #   allowing use of non-Unix forms of "#!cmd". This is intended for
        #   a DOS specific hack only.
        ('skip_source_first_line'    , ctypes.c_int     ),

        # `-c` command line argument
        ('run_command'               , ctypes.c_wchar_p ),

        # `-m` command line argument
        ('run_module'                , ctypes.c_wchar_p ),

        # Trailing command line argument without `-c` or `-m`
        ('run_filename'              , ctypes.c_wchar_p ),

        # --- Private fields ----------------------------

        # Install `importlib`?
        # - If set to 0, `importlib` is not initialized at all.
        # - Needed by `freeze_importlib`.
        ('_install_importlib'        , ctypes.c_int     ),

        # - If equal to 0, stop Python initialization before the "main" phase
        ('_init_main'                , ctypes.c_int     ),

        # - If non-zero, disallow threads, subprocesses, and fork.
        # - Default: 0.
        ('_isolated_interpreter'     , ctypes.c_int     ),

        # Original command line arguments.
        # - If `_orig_argv` is empty and `_argv` is not equal to [''],
        #   `PyConfig_Read()` copies the configuration `argv` list
        #   into `_orig_argv` list before modifying `argv` list
        #   (if `parse_argv` is non-zero).
        # - `_PyConfig_Write()` initializes `Py_GetArgcArgv()` to this list.
        ('_orig_argv'                , PyWideStringList ),
    ]


PyConfig_p = ctypes.POINTER(PyConfig)


###


PyAPI_FUNC("PyConfig_InitPythonConfig",
    argtypes = [
        PyConfig_p,
    ])

PyAPI_FUNC("PyConfig_InitIsolatedConfig",
    argtypes = [
        PyConfig_p,
    ])

PyAPI_FUNC("PyConfig_Clear",
    argtypes = [
        PyConfig_p,
    ])

PyAPI_FUNC("PyConfig_SetString",
    restype = PyStatus,
    argtypes = [
        PyConfig_p,
        ctypes.c_wchar_pp,
        ctypes.c_wchar_p,
    ])

PyAPI_FUNC("PyConfig_SetBytesString",
    restype = PyStatus,
    argtypes = [
        PyConfig_p,
        ctypes.c_wchar_pp,
        ctypes.c_char_p,
    ])

PyAPI_FUNC("PyConfig_Read",
    restype = PyStatus,
    argtypes = [
        PyConfig_p,
    ])

PyAPI_FUNC("PyConfig_SetBytesArgv",
    restype = PyStatus,
    argtypes = [
        PyConfig_p,
        ctypes.py_ssize_t,
        ctypes.c_char_pp,
    ])

PyAPI_FUNC("PyConfig_SetArgv",
    restype = PyStatus,
    argtypes = [
        PyConfig_p,
        ctypes.py_ssize_t,
        ctypes.c_wchar_pp,
    ])

PyAPI_FUNC("PyConfig_SetWideStringList",
    restype = PyStatus,
    argtypes = [
        PyConfig_p,
        PyWideStringList_p,
        ctypes.py_ssize_t,
        ctypes.c_wchar_pp,
    ])


### --- Helper functions ---------------------------------------


PyAPI_FUNC("Py_GetArgcArgv",
    argtypes = [
        ctypes.c_int_p,
        ctypes.c_wchar_ppp,
    ])
